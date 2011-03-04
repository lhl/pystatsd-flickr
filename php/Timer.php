<?php

class Timer {
  static $timers;

  static function start($timer = '_default') {
    self::$timers[$timer] = microtime(true);
  }

  static function stop($timer = '_default') {
    if(self::$timers[$timer]) {
      self::$timers[$timer] = microtime(true) - self::$timers[$timer];
    }
  }

  static function update() {
    if(self::$timers['_default']) {
      $value = self::$timers['_default'] * 1000;
      $server = 'localhost';
      $port = 57475;

      $fp = fsockopen("udp://$server", $port, $errno, $errstr); 
      if($fp) {
        fwrite($fp, "$value");
        fclose($fp);
      }
    }
  }
}


