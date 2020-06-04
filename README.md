# instagrambot

## **Installation**
```elm
pip install instapy
```
__Important:__ depending on your system, make sure to use `pip3` and `python3` instead.


**That's it! 🚀**   
If you're on Ubuntu, read the specific guide on [Installing on Ubuntu (64-Bit)](https://github.com/instagrambot/instagrambot-docs/blob/master/How_Tos/How_To_DO_Ubuntu_on_Digital_Ocean.md). If you're on a Raspberry Pi, read the [Installing on RaspberryPi](https://github.com/instagrambot/instagrambot-docs/blob/master/How_Tos/How_to_Raspberry.md) guide instead.

>If you would like to install a specific version of Instapy you may do so with:
>```elm
>pip install instagrambot==0.1.1
>```

#### Running Instagrambot

To run InstaPy, you'll need to run the **[quickstart](https://github.com/instagrambot/instagrambot-quickstart)** script you've just downloaded.

- [Here is the easiest **quickstart** script you can use](https://github.com/instagrambot/instagrambot-quickstart/blob/master/quickstart.py)  

You can put in your account details now by passing the username and password parameters to the `instagrambot()` function in your **quickstart** script, like so: 
```python
InstaPy(username="abcd", 
        password="1234")
```
Or you can [pass them using the Command Line Interface (CLI)](./DOCUMENTATION.md#pass-arguments-by-cli).

> If you've used _instagrambot_ before installing it by **pip**, you have to move your _old_ data to the new **workspace** folder for on
[Read how to do this here](./DOCUMENTATION.md#migrating-your-data-to-the-workspace-folder).

Once you have your **quickstart** script configured you can execute the script with the following commands.

```elm
python quickstart.py
-- or
python quickstart.py --username abcd --password 1234
```

Instagrambot will now open a browser window and start working.

> If want instagrambot to run in the background pass the `--headless-browser` option when running from the CLI   
Or add the `headless_browser=True` parameter to the `Instagrambot(headless_browser=True)` constructor.

#### Updating instagrambot
```elm
pip install instagrambot -U
```


## Guides

#### Video tutorials:
**soon**


## Documentation
A list of **all features** of Instagrambot [can be found here](./DOCUMENTATION.md). 



> **Disclaimer**<a name="disclaimer" />: Please Note that this is a research project. I am by no means responsible for any usage of this tool. Use on your own behalf. I'm also not responsible if your accounts get banned due to extensive use of this tool.
