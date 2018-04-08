## Draw Moon Phases

![Imgur Image](http://i.imgur.com/kkomq8x.png)

### Usage

``` python
import math
import moon
from draw_moon import draw_moon

m = moon.MoonPhase()
draw_moon(math.radians(m.angle), offset_x, offset_y, width, height, path_to_image)
```