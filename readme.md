# Blend Stats for PHP

This is a small class/lib for PHP which lets users read file stats from blend files using blender through the command line interface for usage in blender related sites.

Blend Stats calls the Blender binary in your system path and then executes a python script which retrieves some basic stats from the passed file.

## Usage:

```php
<?php

// include the lib
include '/path/to/blend_stats.php';

// INSTANTIATE
// pass blend location immediately [*]
$bst = new BlendStats( '/path/to/blend/file.blend' );

// get the stats
$blendStats = $bst->get_stats();

// use the stats
$blend['statistics'] = $blendStats->stats;

// Save to database? Save to File? Whatever you to do.

?>
```


## Notes:

[*] there's a second argument for the constructor with which the Blender binary call is passed; it defaults to `'blender'` and works just fine if you have Blender in your System PATH so this arg is optional. If for some reason you can't have Blender added to your System PATH var, then you should pass the path to your local Blender binary in the second parameter of the constructor; for example:

```php
<?php 

// ON WINDOWS:
$bst = new BlendStats('C:\\path\\to\\file.blend', 'C:\\path\\to\\blender\\blender');

// ON POSIX
$bst = new BlendStats('/path/to/file.blend', '/path/to/blender');

?>
```

* This lib is rather slow, and you might need a lot of RAM on your server to run it with acceptable performance.