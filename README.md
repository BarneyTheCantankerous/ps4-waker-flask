# ps4-waker-flask
Simple Python Flask server to handle web requests for [ps4-waker](https://www.npmjs.com/package/ps4-waker).

This project mostly lives on an old Raspberry Pi B, that I finally put to use! With the intention of using it with IFTTT and Google Assistant to extend home automation and ask Google to kindly turn on/off my PS4. 

# Next Steps
- Overhaul the code
- Extend waker to make use of store search
- Strengthen security
	- Move to using HTTPS
	- Convert URL paths to HTTP GET/POST requests 
	- Use some kind of authentication when receiving requests
- Make use of Google Assistant SDK
	- PS apps can be opened
	- Store search results can load found PS apps