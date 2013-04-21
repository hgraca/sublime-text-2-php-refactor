<?php

class Calculator
{

    public $test = 0;

    public function calculate($a, $b, $op)
    {
        if ($op == '+'){
            $result = $a + $b;
        }
        return $result;
    }
}