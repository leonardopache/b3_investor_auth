# B3 Investor Authentication #

This package do the authentication in the investor area of [B3](https://cei.b3.com.br/). 
- For this first version the authentication is using Selenium and for that the return is a webdriver. 

### What is this repository for? ###

* Implementation of authentication of investor
* v0.1

### How do I get set up? ###

* Setup it locally:
  - Checkout the source code;
  - install with ***pip install .*** from repository home or add ***b3-investor-auth==0.1*** in requirements.txt
* Usage
  - Initialize Authorization(**path_chrome_driver**, lang=LANG_EN, headless=True)
  - then call login(user, pwd) or logout()
* Dependencies
  - look for requirements.txt 
* How to run tests
  - not implemented 
  
### What are coming next? ###
- [ ] factory to chose different authentication protocol
- [ ] more stable implementation for solve the **recaptcha challenge**
- [ ] improve test

### Who do I talk to? ###

* leonardo pache
* https://github.com/leonardopache
