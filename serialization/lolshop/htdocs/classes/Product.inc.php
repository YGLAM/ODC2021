<?php

class Product {

    private $id;
    private $name;
    private $description;
    private $picture;
    private $price;

    function __construct($id, $name, $description, $picture, $price) {
        $this->id = $id;
        $this->name = $name;
        $this->description = $description;
        $this->picture = $picture;
        $this->price = $price;
    }

    function getId() {
        return $this->id;
    }

    function getName() {
        return $this->name;
    }

    function getDescription() {
        return $this->description;
    }

    function getPicture() {
        $path = '/var/www/assets/' . $this->picture;
        $data = base64_encode(file_get_contents($path));
        return $data;
        // this might be exploited !!
    }

    function getPrice() {
        return $this->price;
    }

    function toDict() {
        return array(
            "id" => $this->id,
            "name" => $this->name,
            "description" => $this->description,
            "picture" => $this->getPicture(),
            "price" => $this->price
        );
        //also this one , it is found inside
    }

}

?>
