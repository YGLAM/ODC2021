<?php

class State {

    private $session;
    private $cart;

    function __construct($session) {
        $this->session = $session;
        $this->cart = array();
    }

    function getSessionID() {
        return $this->session->getId();
    }

    function getSession() {
        return $this->session;
    }

    function getCart() {
        return $this->cart;
    }

    function clearCart() {
        $this->cart = array();
    }

    function addToCart($product_id) {
        if(array_key_exists($product_id, $this->cart)) {
            $this->cart[$product_id]++;
        } else {
            $this->cart[$product_id] = 1;
        }
    }

    function toDict() {
        $out = array();
        foreach($this->cart as $product_id => $quantity) {
            array_push($out, array("product" => $product_id, "quantity" => $quantity));
        }
        return array("name" => $this->session->getName(), "email" => $this->session->getEmailAddress(), "cart" => $out);
        //Both State and Product have a toDict() method so if the objects were to be swapped the call
        // would still work ! 
    }


    function save() {
        return base64_encode(gzcompress(serialize($this)));
        //base64 + gzcompress + serialize
        //so if we go through these steps we can craft a malicious Object
        //you should understand where this object is deserialized
    }

    static function restore($token) {
        return unserialize(gzuncompress(base64_decode($token)));
        //this is the deserialization function
    }

}

?>
