<?php

class Calculator
{
    public function calculate($a, $b, $op)
    {
        if ($op == '+'){
            $result = $a + $b;
        }
        return $result;
    }
}