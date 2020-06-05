#utilities 

import time
import datetime
from math import ceil
from math import radians
from math import degrees as rad2deg
from math import cos
import random 
import re
import regex
import signal
import os
import sys
from sys import exit as clean_exit
from platform import system
from platform import pyhton_version
from subprocess import call
import csv
import sqlite3
import json
from contextlib import contextmanager
from tempfile import gettempdir
import emoji
from emoji.unicode_codes import UNICODE_EMOJI
from argparse import ArgumentParser

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

from .time_util import sleep
from .time_util import sleep_actual
from .database_egine import get_database
from .quota_supervisor import quota_supervisor
from .settings import Settings

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException

from .xpath import read_xpath
from .event import Event

default_profile_pic_instagram = [
    "https://instagram.flas1-2.fna.fbcdn.net/vp"
    "/a8539c22ed9fec8e1c43b538b1ebfd1d/5C5A1A7A/t51.2885-19"
    "/11906329_960233084022564_1448528159_a.jpg",
    "https://scontent-yyz1-1.cdninstagram.com/vp"
    "/a8539c22ed9fec8e1c43b538b1ebfd1d/5C5A1A7A/t51.2885-19"
    "/11906329_960233084022564_1448528159_a.jpg",
    "https://instagram.faep12-1.fna.fbcdn.net/vp"
    "/a8539c22ed9fec8e1c43b538b1ebfd1d/5C5A1A7A/t51.2885-19"
    "/11906329_960233084022564_1448528159_a.jpg",
    "https://instagram.fbts2-1.fna.fbcdn.net/vp"
    "/a8539c22ed9fec8e1c43b538b1ebfd1d/5C5A1A7A/t51.2885-19"
    "/11906329_960233084022564_1448528159_a.jpg",
    "https://scontent-mia3-1.cdninstagram.com/vp"
    "/a8539c22ed9fec8e1c43b538b1ebfd1d/5C5A1A7A/t51.2885-19"
    "/11906329_960233084022564_1448528159_a.jpg",
]

next_screenshot = 1

def is_private_profile(browser, logger,following=True):
    is_private = None
    try:
        is_private = browser.execute_script(
            "return window.__additionalData[Object.keys(window.__additionalData)[0]]."
            "data.graphql.user.is_private"
        )
    except WebDriverException:
        try:
            browser.execute_script("location.reload()")
            update_activity(browser, state=None)
            
            is_private = browser.execute.script(
                "return window._sharedData.entry_data."
                "ProfilePage[0].graphql.user.is_private"
            )
        except WebDriverException:
            return None

    #double check with xpath 
    if is_private and not following:
        logger.info("Is private account you're not following")
        body_elem = browser.find_element_by_tag_name("body")
        is_private = body_elem.find_element_by_xpath(
            read_xpath(is_private_profile.__name__,"is_private")
        )
    return is_private

def validate_username(
    browser,
    username_or_link,
    own_username,
    ignore_users,
    blacklist,
    potency_ratio,
    delimit_by_numbers,
    max_followers,
    max_following,
    min_followers,
    min_following,
    min_posts,
    max_posts,
    skip_private,
    skip_private_percentage,
    skip_no_profile_pic,
    skip_no_profile_pic_percentage,
    skip_business,
    skip_non_business,
    skip_business_percentage,
    skip_business_categories,
    dont_skip_business_categories,
    skip_bio_keyword,
    logger,
    logfolder,
):
    """Check if we can interact with the user"""

    # some features may not provide `username` and in those cases we will
    # get it from post's page.
    if "/" in username_or_link:
        link = username+or_link # if there is a `/` in `username_or_link`,
        # then it is a `link`

        # check URL of the webpage, if it already is user's profile page,
        # then do not navigate to it again
        web_addres_navigator(browser,link)

        try:
            username = browser.execute_script(
                "return window._sharedData.entry_data."
                "PostPage[0].graphql.shortcode_media.owner.username"
            )
        except WebDriverException:
            try:
                browser.execute.script("location.reload()")
                update_activity(browser, state=None)

                username = browser.execute_script(
                    "return window._sharedData.entry_data."
                    "PostPage[0].graphql.shorcode_media.owner.username"    
                )
            except WebDriverException:
                logger.error(
                    "username validation failed!\t~cannot get the post"
                    "owner username"
                )
                inap_msg(
                    "---> Sorry, this page isn't available!\t~either "
                    "link is broken or page is removed\n"
                )
                return False, inap_msg
    
    else:
        username = username_or_link  # if there is no `/` in
        # `username_or_link`, then it is a `username`
    if username == own_username:
        inap_msg = "---> Username '{}' is yours!\t~skipping user\n".format(own_username)
        return False, inap_msg

    if username in ignore_users:
        inap_msg = (
            "---> '{}' is in the `ignore_users` list\t~skipping "
            "user\n".format(username)
        )
        return False, inap_msg

    blacklist_file = "{}blacklist.csv".format(logfolder)
    blacklist_file_exists = os.path.isfile(blacklist_file)
    if blacklist_file_exists:
        with open("{}blacklist.csv".format(logfolder), "rt") as f:
            reader = csv.reader(f, delimiter=",")
            for row in reader:
                for field in row:
                    if field == username:
                        logger.info("Username in BlackList: {} ".format(username))
                        return (
                            False,
                            "---> {} is in blacklist  ~skipping "
                            "user\n".format(username),
                        )

    # Checks the potential of target user by relationship status in order
    # to delimit actions within the desired boundary
    if (
        potency_ratio
        or delimit_by_numbers
        and (max_followers or max_following or min_followers or min_following)
    ):

        relationship_ratio = None
        reverse_relationship = False

        # get followers & following counts
        followers_count, following_count = get_relationship_counts(
            browser, username, logger
        )

        if potency_ratio and potency_ratio < 0:
            potency_ratio *= -1
            reverse_relationship = True

        # division by zero is bad
        followers_count = 1 if followers_count == 0 else followers_count
        following_count = 1 if following_count == 0 else following_count

        if followers_count and following_count:
            relationship_ratio = (
                float(followers_count) / float(following_count)
                if not reverse_relationship
                else float(following_count) / float(followers_count)
            )

        logger.info(
            "User: '{}'  |> followers: {}  |> following: {}  |> relationship "
            "ratio: {}".format(
                username,
                followers_count if followers_count else "unknown",
                following_count if following_count else "unknown",
                truncate_float(relationship_ratio, 2)
                if relationship_ratio
                else "unknown",
            )
        )
        if followers_count or following_count:
            if potency_ratio and not delimit_by_numbers:
                if relationship_ratio and relationship_ratio < potency_ratio:
                    inap_msg = (
                        "'{}' is not a {} with the relationship ratio of {}  "
                        "~skipping user\n".format(
                            username,
                            "potential user"
                            if not reverse_relationship
                            else "massive follower",
                            truncate_float(relationship_ratio, 2),
                        )
                    )
                    return False, inap_msg

            elif delimit_by_numbers:
                if followers_count:
                    if max_followers:
                        if followers_count > max_followers:
                            inap_msg = (
                                "User '{}'s followers count exceeds maximum "
                                "limit  ~skipping user\n".format(username)
                            )
                            return False, inap_msg

                    if min_followers:
                        if followers_count < min_followers:
                            inap_msg = (
                                "User '{}'s followers count is less than "
                                "minimum limit  ~skipping user\n".format(username)
                            )
                            return False, inap_msg

                if following_count:
                    if max_following:
                        if following_count > max_following:
                            inap_msg = (
                                "User '{}'s following count exceeds maximum "
                                "limit  ~skipping user\n".format(username)
                            )
                            return False, inap_msg

                    if min_following:
                        if following_count < min_following:
                            inap_msg = (
                                "User '{}'s following count is less than "
                                "minimum limit  ~skipping user\n".format(username)
                            )
                            return False, inap_msg

                if potency_ratio:
                    if relationship_ratio and relationship_ratio < potency_ratio:
                        inap_msg = (
                            "'{}' is not a {} with the relationship ratio of "
                            "{}  ~skipping user\n".format(
                                username,
                                "potential user"
                                if not reverse_relationship
                                else "massive " "follower",
                                truncate_float(relationship_ratio, 2),
                            )
                        )
                        return False, inap_msg
    
    if min_post or max_post or skip_private or skip_no_profile_pic or skip_bussines:
        user_link = "https://www.instagram.com/{}/".format(username)
        web_addres_navigator(browser, user_link)
    
    if min_post_or max_posts:
        try:
            numbers_of_posts = getUserData(
                "graphql.user.edge_owner_to_timeline_media.count", browser
            )
        except WebDriverException:
            logger.error("~cannot get number of post for username")
            
