'''
Roulette
========

:class:`Roulette` provides a rolling way of selecting values like in iOS
and android date pickers.

Dependencies
------------

*. the garden package ``kivy.garden.tickline``. Use ``garden install tickline``
    to install it like any other garden package.

*. the garden package ``kivy.garden.roulettescroll``.

Usage
-----

It's simple to use. To give a choice from 0, 1, ..., 9, use::

    CyclicRoulette(cycle=10, zero_indexed=True)

Or if we need to select a year, with the default value being the current one,
we can use::

    year_roulette = Roulette()
    year_roulette.select_and_center(datetime.now().year)

:class:`CyclicRoulette` inherits from :class:`Roulette`, so any setting
pertaining to :class:`Roulette` also applies to :class:`CyclicRoulette`.

If the values need to be formatted, pass the desired format spec string to
:attr:`Roulette.format_spec`, like so::

    CyclicRoulette(cycle=60, zero_indexed=True, format_spec='{:02d}'}

This configuration is used much for time display, so there's a convenience
class :class:`TimeFormatCyclicRoulette` for it, with ``zero_index=True``
and ``format_spc='{:02d}'``.

:attr:`Roulette.density` controls how many values are displayed. To show
3 values at a time, pass ``density=3``. Fractional values will partially
hide values on the edges.

Here's a complete working example with all of the concepts above, a
primitive datetime selector::

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

:attr:`Roulette.selected_value` contains the current selection. When the
roulette is still, this is the number at the center. If the roulette is
moving, this is the last number centered on before the roulette started
moving.

If you need more real time information on the value selection, you may
confer :attr:`Roulette.rolling_value`. This is the value the would be selected
if the roulette were to stop right now. So if the roulette is not moving,
then :attr:`Roulette.rolling_value` is equal to :attr:`Roulette.selected_value`.
Otherwise, they are expected to be different. Note, however, that this
value is not stable to widget resizing, as is ``selected_value``.

To center the roulette, you can call :meth:`Roulette.center_on`. This method
performs an animation to center on the desired value. It does NOT change the
:attr:`~Roulette.selected_value`. The method mentioned above,
:attr:`~Roulette.select_and_center`, on the other hand, does change
the selected value.

To integrate the roulette animations with other UI elements, it may be necessary
to specially handle the :meth:`Roulette.center_on` animation. The event
:meth:`Roulette.on_center` can be listened for. It signals the completion
of the ``center_on`` animation.

NICER GRAPHICS!
---------------

I didn't focus much on the graphics, or to closely simulate the iOS or android
experience. You are encourage to contribute to improve the default appearance
of the roulette!

    .. versionchanged:: 0.1.1

           a background image can be added by giving the path
            to :attr:`Roulette.background_image`.

Extending
---------

:class:`Roulette` inherits from :class:`kivy.garden.tickline.Tickline`, and
as such, uses its system of tickline, tick, and labeller. Hence extensive
customizations may be done by extending :class:`Slot` and :class:`CyclicSlot`,
the default tick classes of respectively :class:`Roulette` and
:class:`CyclicRoulette`, and :class:`SlotLabeller`, the default labeller class
of :class:`Roulette`.

'''

__version__ = '0.1.1'

from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.text import Label as CoreLabel
from kivy.garden.roulettescroll import RouletteScrollEffect
from kivy.garden.tickline import Tick, Tickline, TickLabeller
from kivy.graphics.vertex_instructions import Rectangle
from kivy.lang import Builder
from kivy.metrics import sp, dp
from kivy.properties import ListProperty, ObjectProperty, AliasProperty, \
    NumericProperty, BooleanProperty, StringProperty, OptionProperty
from kivy.graphics.vertex_instructions import BorderImage
from os.path import join, dirname


class SlotLabeller(TickLabeller):
    def __init__(self, tickline):
        self.instructions = {}
        self.re_init()
        self.tickline = tickline

    def re_init(self):
        self.to_pop = set(self.instructions)
        self.to_push = []

    def register(self, tick, tick_index, tick_info):
        tickline = self.tickline
        if tick_index not in self.instructions:
            self.to_push.append(tick_index)
            texture = tick.get_label_texture(tick_index)
        else:
            self.to_pop.remove(tick_index)
            texture = self.instructions[tick_index].texture
        if texture:
            if tickline.is_vertical():
                tick_pos = tick_info[1] + tick_info[3] / 2
                pos = (tickline.center_x - texture.width / 2,
                       tick_pos - texture.height / 2)
            else:
                tick_pos = tick_info[0] + tick_info[2] / 2
                pos = (tick_pos - texture.width / 2,
                       tickline.center_y - texture.height / 2)
            # only need to update the position if label is saved
            self.instructions.setdefault(tick_index,
                Rectangle(texture=texture, size=texture.size,
                          group=self.group_id)).pos = pos

    def make_labels(self):
        canvas = self.tickline.canvas
        for index in self.to_push:
            rect = self.instructions[index]
            canvas.add(rect)
        for index in self.to_pop:
            rect = self.instructions.pop(index)
            canvas.remove(rect)

#===============================================================================
# Slots
#===============================================================================

class Slot(Tick):
    tick_size = ListProperty([0, 0])
    font_size = NumericProperty('20sp')
    int_valued = BooleanProperty(True)
    format_str = StringProperty('{}')
    def value_str(self, value):
        return self.format_str.format(value)
    def slot_value(self, index, *args, **kw):
        '''returns the selection value that corresponds to ``index``.
        Should be overriden if necessary.'''
        if self.int_valued:
            return int(round(index))
        return index
    def index_of(self, val, *args, **kw):
        '''returns the index that corresponds to a selection value ``val``.
        Should be override if necessary.'''
        return val
    def get_label_texture(self, index, **kw):
        label = CoreLabel(text=self.value_str(self.slot_value(index)),
                          font_size=self.font_size, **kw)
        label.refresh()
        return label.texture

class CyclicSlot(Slot):
    cycle = NumericProperty(10)
    zero_indexed = BooleanProperty(False)

    def get_first_value(self):
        return 0 if self.zero_indexed else 1
    def set_first_value(self, val):
        self.zero_indexed = not val
    first_value = AliasProperty(get_first_value, set_first_value, cache=True,
                                bind=['zero_indexed'])
    '''provides a default value.'''

    def slot_value(self, index):
        cycle = self.cycle
        val = index % cycle + 1 - self.zero_indexed
        val = Slot.slot_value(self, val)
        if val >= cycle + 1 - self.zero_indexed:
            val -= cycle
        return val

    def index_of(self, val, current_index, *args, **kw):
        '''returns the closest index to ``current_index`` that would correspond
        to ``val``. All indices should be localized.'''
        if self.int_valued:
            val = int(round(val))
        zero_indexed = self.zero_indexed
        cycle = self.cycle
        if not (1 - zero_indexed) <= val <= cycle - zero_indexed:
            raise ValueError('value must be between {} and {}; {} is given'.
                             format(1 - zero_indexed, cycle - zero_indexed, val))
        base_index = val - 1 + self.zero_indexed
        n = round((current_index - base_index) / cycle)
        index = n * cycle + base_index
        return index


#===============================================================================
# Roulettes
#===============================================================================

class Roulette(Tickline):
    __events__ = ('on_centered',)

    #===========================================================================
    # overrides
    #===========================================================================

    background_image = StringProperty(
                        join(dirname(__file__), 'roulettebackground.png'),
                        allownone=True)
    '''background image, overriding the default of None in :class:`Tickline`.

    .. versionadded:: 0.1.1
    '''

    background_color = ListProperty([1, 1, 1, 1])
    '''background color, defaulting to [1, 1, 1, 1], overriding default
    of [0, 0, 0] in :class:`Tickline`.

    .. versionadded:: 0.1.1
    '''

    cover_background = BooleanProperty(False)
    '''determines whether to draw a Rectangle covering the background.
    Overriding :class:`Tickline` default to give False.

    .. versionadded:: 0.1.1
    '''

    size_hint_x = NumericProperty(None, allownone=True)
    labeller_cls = ObjectProperty(SlotLabeller)
    zoomable = BooleanProperty(False)
    draw_line = BooleanProperty(False)
    font_size = NumericProperty('20sp')
    width = NumericProperty('60dp')

    # doesn't make sense to have more than 1 tick
    tick = ObjectProperty(None)

    def get_ticks(self):
        if self.tick:
            return [self.tick]
        else:
            return []
    def set_ticks(self, val):
        self.tick = val[0]
    ticks = AliasProperty(get_ticks, set_ticks, bind=['tick'])

    #===========================================================================
    # public attributes
    #===========================================================================

    selected_value = ObjectProperty(None)
    '''the currently selected value.'''

    format_str = StringProperty('{}')
    '''formatting spec string for the values displayed.'''

    tick_cls = ObjectProperty(Slot)
    '''The class of the tick in this roulette. Defaults to
    :class:`Slot`. Should be overriden as needed by child class.'''

    int_valued = BooleanProperty(True)
    '''indicates whether the values should be displayed as integers.'''

    scroll_effect_cls = ObjectProperty(RouletteScrollEffect)

    # has to be negative so that ``ScrollEffect.trigger_velocity_update``
    # is always called
    drag_threshold = NumericProperty(-1)
    '''this is passed to the ``drag_threshold`` of :attr:`scroll_effect_cls`.

    It is by default set to -1 to turn off the drag threshold.
    '''

    center_duration = NumericProperty(.3)
    '''duration for the animation of :meth:`center_on`.'''

    density = NumericProperty(4.2)
    '''determines how many slots are shown at a time.'''

    def get_rolling_value(self):
        return self.tick.slot_value(self.tick.localize(self.index_mid))
    def set_rolling_value(self, val):
        self.index_mid = self.tick.globalize(val)
    rolling_value = AliasProperty(get_rolling_value,
                                    set_rolling_value,
                                    bind=['index_mid'])
    '''the val indicated by whatever slot is in the middle of the roulette.
    If the roulette is still, then :attr:`rolling_value` is equal to
    :attr:`selected_value`. Otherwise, they shouldn't be equal.

    .. note::
        This property is not stable under resizing, since often that will
        change the slot in the middle.'''


    def __init__(self, **kw):
        self.tick = Slot()
        self._trigger_set_selection = \
                Clock.create_trigger(self.set_selected_value)
        super(Roulette, self).__init__(**kw)
        self.scale = dp(10)
        self.tick = self.tick_cls()
        self._trigger_calibrate()

    def on_tick_cls(self, *args):
        self.tick = self.tick_cls()
    def on_tick(self, *args):
        tick = self.tick
        if tick:
            tick.font_size = self.font_size
            tick.int_valued = self.int_valued
            tick.format_str = self.format_str
    def on_size(self, *args):
        self.scale = self.line_length / self.density
        self.recenter()
    def on_int_valued(self, *args):
        if self.tick:
            self.tick.int_valued = self.int_valued
    def on_format_str(self, *args):
        if self.tick:
            self.tick.format_str = self.format_str

    def get_anchor(self):
        '''returns a legal stopping value for the :class:`RouletteScrollEffect`.
        Should be overriden if necessary.'''
        return 0
    def _update_effect_constants(self, *args):
        if not super(Roulette, self)._update_effect_constants(*args):
            return
        effect = self.scroll_effect
        scale = self.scale
        effect.pull_back_velocity = sp(50) / scale
    def calibrate_scroll_effect(self, *args, **kw):
        if not super(Roulette, self).calibrate_scroll_effect(*args, **kw):
            return
        anchor = self.get_anchor()
        effect = self.scroll_effect
        effect.interval = 1. / self.tick.scale_factor
        effect.anchor = anchor
        effect.on_coasted_to_stop = self._trigger_set_selection
    def set_selected_value(self, *args):
        '''set :attr:`selected_value` to the currently slot.'''
        self.selected_value = self.round_(self.rolling_value)
    def round_(self, val):
        '''round an arbitrary rolling value to a legal selection value.
        Should be overriden if necessary.'''
        if self.int_valued:
            return int(round(val))
        return round(val)
    def recenter(self, *args):
        if self.selected_value is not None:
            self.center_on(self.selected_value)
        self._trigger_calibrate()
    def index_of(self, val):
        '''returns the index that should be equivalent to a selection value
        ``val``. Should be overriden if necessary.'''
        return val
    def center_on(self, val, animate=True):
        Animation.stop_all(self)
        center_index = self.index_of(val)
        half_length = self.line_length / 2. / self.scale
        index_0 = center_index - half_length
        index_1 = center_index + half_length
        if animate:
            anim = Animation(index_0=index_0, index_1=index_1,
                             duration=self.center_duration)
            anim.on_complete = lambda *args: self._centered()
            anim.start(self)
        else:
            self.index_0 = index_0
            self.index_1 = index_1
            self._centered()
    def on_centered(self, *args):
        '''event that fires when the operation :meth:`center_on` completes.
        (and by extension, when :meth:`center` or :meth:`select_and_center`
        completes). By default it doesn't do anything.'''
        pass

    def _centered(self, *args):
        self._trigger_calibrate()
        self.dispatch('on_centered')
    def center(self, animate=True):
        self.center_on(self.selected_value, animate)
    def select_and_center(self, val, *args, **kw):
        '''set :attr:`selected_value` to ``val`` and center on it. If
        :attr:`selected_value` is already ``val``, return False; else return
        True.'''
        if self.selected_value == val:
            return False
        self.selected_value = val
        self.center(*args, **kw)
        return True
    def is_rolling(self):
        return self.scroll_effect.velocity != 0

class CyclicRoulette(Roulette):
    '''roulette for displaying cyclic values.'''
    tick_cls = ObjectProperty(CyclicSlot)

    cycle = NumericProperty(10)
    '''the cycle of values displayed.'''

    zero_indexed = BooleanProperty(False)
    '''whether the values displayed will start from 0 or 1.'''

    def __init__(self, **kw):
        super(CyclicRoulette, self).__init__(**kw)
        self.selected_value = self.tick.first_value
        self.center()

    def on_tick(self, *args):
        tick = self.tick
        if tick:
            tick.cycle = self.cycle
            tick.zero_indexed = self.zero_indexed
        super(CyclicRoulette, self).on_tick(*args)
    def on_cycle(self, *args):
        if self.tick:
            self.tick.cycle = self.cycle
    def on_zero_indexed(self, *args):
        if self.tick:
            self.tick.zero_indexed = self.zero_indexed
    def index_of(self, val):
        tick = self.tick
        if not tick:
            return val
        return tick.index_of(val, tick.localize(self.index_mid))


class TimeFormatCyclicRoulette(CyclicRoulette):
    '''formatted roulette for displaying time.'''
    zero_indexed = BooleanProperty(True)
    format_str = StringProperty('{:02d}')

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

