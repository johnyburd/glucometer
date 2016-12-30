Roulette
========

`Roulette` provides a rolling way of selecting values like in iOS
and android date pickers. 

Dependencies
------------

*. the garden package ``kivy.garden.tickline``. Use ``garden install tickline``
    to install it like any other garden package.

*. the garden package ``kivy.garden.roulettescroll``.

Usage
-----

It's simple to use. To give a choice from 0, 1, ..., 9, use

    CyclicRoulette(cycle=10, zero_indexed=True)

Or if we need to select a year, with the default value being the current one,
we can use

    year_roulette = Roulette()
    year_roulette.select_and_center(datetime.now().year)
    
`CyclicRoulette` inherits from `Roulette`, so any setting
pertaining to `Roulette` also applies to `CyclicRoulette`.

If the values need to be formatted, pass the desired format spec string to
`Roulette.format_spec`, like so

    CyclicRoulette(cycle=60, zero_indexed=True, format_spec='{:02d}'}
    
This configuration is used much for time display, so there's a convenience
class `TimeFormatCyclicRoulette` for it, with ``zero_index=True``
and ``format_spec='{:02d}'``. 

`Roulette.density` controls how many values are displayed. To show
3 values at a time, pass ``density=3``. Fractional values will partially
hide values on the edges. 

Here's a complete working example with all of the concepts above, a
primitive datetime selector

    if __name__ == '__main__':
        from kivy.base import runTouchApp
        from kivy.uix.boxlayout import BoxLayout
        from kivy.garden.roulette import Roulette, CyclicRoulette, \
            TimeFormatCyclicRoulette
        
        b = BoxLayout()
        b.add_widget(Roulette(density=2.8, selected_value=2013))
        b.add_widget(CyclicRoulette(cycle=12, density=2.8, zero_indexed=False))
        b.add_widget(CyclicRoulette(cycle=30, density=2.8, zero_indexed=False))
        b.add_widget(TimeFormatCyclicRoulette(cycle=24))
        b.add_widget(TimeFormatCyclicRoulette(cycle=60)) 
        b.add_widget(TimeFormatCyclicRoulette(cycle=60)) 
        
        runTouchApp(b)

`Roulette.selected_value` contains the current selection. When the 
roulette is still, this is the number at the center. If the roulette is
moving, this is the last number centered on before the roulette started 
moving.

If you need more real time information on the value selection, you may
confer `Roulette.rolling_value`. This is the value the would be selected
if the roulette were to stop right now. So if the roulette is not moving,
then `Roulette.rolling_value` is equal to `Roulette.selected_value`.
Otherwise, they are expected to be different. Note, however, that this
value is not stable to widget resizing, as is ``selected_value``. 

For example, we can check the selected and rolling values of the above snippet
with::


	if __name__ == '__main__':
	    from kivy.base import runTouchApp
	    from kivy.uix.boxlayout import BoxLayout
	    from kivy.uix.label import Label
	    b = BoxLayout()
	    b.add_widget(Roulette(density=2.8, selected_value=2013))
	    b.add_widget(CyclicRoulette(cycle=12, density=2.8, zero_indexed=False))
	    b.add_widget(CyclicRoulette(cycle=30, density=2.8, zero_indexed=False))
	    b.add_widget(TimeFormatCyclicRoulette(cycle=24))
	    b.add_widget(TimeFormatCyclicRoulette(cycle=60)) 
	    b.add_widget(TimeFormatCyclicRoulette(cycle=60)) 
	    selected_value = Label()
	    rolling_value = Label()
	    for c in b.children:
	        c.bind(selected_value=lambda _, val:
	               selected_value.setter('text')(_,
	                'selected_value:\n' + str(val)),
	               rolling_value=lambda _, val:
	               rolling_value.setter('text')(_,
	                'rolling_value:\n' + str(val)))
	    
	    b.add_widget(selected_value)
	    b.add_widget(rolling_value)
	    
	    runTouchApp(b)
    
To center the roulette, you can call `Roulette.center_on`. This method
performs an animation to center on the desired value. It does NOT change the
`Roulette.selected_value`. The method mentioned above, 
`Roulette.select_and_center`, on the other hand, does change 
the selected value. 

To integrate the roulette animations with other UI elements, it may be necessary
to specially handle the `Roulette.center_on` animation. The event
`Roulette.on_center` can be listened for. It signals the completion
of the ``center_on`` animation. 

NICER GRAPHICS!
---------------

I didn't focus much on the graphics, or to closely simulate the iOS or android
experience. You are encourage to contribute to improve the default appearance
of the roulette!

In version 0.1.1 and later, a background image can be added by giving the path
to `Roulette.background_image`.

Extending
---------

`Roulette` inherits from `kivy.garden.tickline.Tickline`, and
as such, uses its system of tickline, tick, and labeller. Hence extensive
customizations may be done by extending `Slot` and `CyclicSlot`,
the default tick classes of respectively `Roulette` and 
`CyclicRoulette`, and `SlotLabeller`, the default labeller class 
of `Roulette`.
 