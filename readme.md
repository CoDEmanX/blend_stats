# Blend Stats for PHP

This is a small class/lib for PHP which lets users read file stats from blend files using blender through the command line interface for usage in blender related sites.

Blend Stats calls the Blender binary in your system path and then executes a python script which retrieves some basic stats from the passed file.

## Usage:

```php
<?php

// include the lib
include('/path/to/blend_stats.php');

// INSTANTIATE
// pass blend location and callable Blender bin[*]
$bst = new BlendStats('/path/to/blend/file.blend', 'blender');

// get the stats
$blendStats = $bst->get_stats();

// use the stats
$blend['statistics'] = $blendStats->stats;

// Save to database? - Save to File? - Whatever you feel like doing.

?>
```


## Notes:

* [*] The Blender bin arg is optional, it defaults to `'blender'` and assuming you have blender added to your System PATH there's no problem. If you have blender installed as portable, or do not want or cannot to include in your System PATH, you must pass the full path to the blender binary in the second argument of the BlendStats() call.

* This lib is rather slow, and you might need a lot of RAM on your server to run it with acceptable performance.