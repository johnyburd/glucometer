'''
Tickline
========

The :class:`Tickline` widget is designed to display a stream of measured data.

For example, a ruler-like :class:`Tickline` can 
display a tick every 10 pixels. A timeline-like :class:`Tickline` can display
dates and hours. If you have some 2-dimensional data, you can also use 
:class:`Tickline` to graph it against ticks demarcating some interval.

What makes :class:`Tickline` amazing is the ability to zoom and pan, and 
automatically adjust the ticks displayed in response to changing scale. 
If my tickline has multiple ticks, the ticks that are too fine will not 
be displayed. If I zoom in too much, I can always scroll it to see other parts 
of the tickline.

Usage
-----

A :class:`Tickline` by itself doesn't display anything other than perhaps
a line along its direction. It needs to be given :class:`Tick`s to draw. The
attribute :attr:`Tickline.ticks` contains a list of :class:`Tick`s that will
be displayed. 

Here is a simple example that will display ticks with integer labels::

    Tickline(ticks=[Tick()])

The power of :class:`Tickline` really comes through with multiple :class:`Tick`s
though. The following is a :class:`Tickline` that displays ticks with intervals
of 1, 1/5, and 1/10::

    Tickline(ticks=[Tick(), Tick(scale_factor=5.), Tick=(scale_factor=10.)])
    
You may notice that the :class:`Tick`s all label themselves by their *own* 
numbers, instead of, for example, the 1/5 tick labelling by 1/5 and the 1/10
tick labelling by 1/10. The 1/5, 2/5, 3/5, ... or 1/10, 2/10, ... would be
the *global indices* of the ticks. By default, however, the ticks are labelled
by *local indices*. This can be changed by setting :attr:`Tick.label_global` 
to True. 

A setting of interest may be :attr:`Tick.offset`, which causes the :class:`Tick`
to be draw at local indices ``..., offset - 2, offset - 1, offset, 
offset + 1, offset + 2, ...``.

Whether the tick*line* is displayed can be toggled with 
:attr:`Tickline.draw_line`, and its position can be set via
:attr:`Tickline.line_offset` and :attr:`Tickline.line_pos`. Other attributes
like :attr:`Tickline.line_color`, :attr:`Tickline.line_width`, 
and :attr:`Tickline.background_color` do what their names suggest to do.

If the tick*line* is drawn, the settings :attr:`Tick.halign` and 
:attr:`Tick.valign` can be used to specify where the tick is rendered. In short,
if the line is vertical, then ``halign`` is used, and can be one of
'left', 'right', 'line_left', 'line_right'. If the line is horizontal, then
``valign`` is used, and can be one of 'top', 'bottom', 'line_top', 

If you'd like not to label a set of ticks, for example, like the milimeter ticks
on a typical ruler, then use :class:`LabellessTick`. 

If you'd like to draw ticks for only some numbers, use :class:`DataListTick`.

To put it all together::

    Tickline(ticks=[Tick(tick_size=[4, 20], offset=.5),
                    Tick(scale_factor=5., label_global=True),
                    LabellessTick(tick_size=[1, 4], scale_factor=25.),
                    DataListTick(data=[-0.3, 1, 1.5, 2, 4, 8, 16, 23],
                                 scale_factor=5.,
                                 halign='line_right',
                                 valign='line_top')
                    ],
             orientation='horizontal',
             backward=True)
            
Here's a :class:`Tickline` with 4 ticks drawn; 
the first set with interval of 1, the second, 1/5, the third, 1/25, and
the final set has ticks at the local indices provided by the list (so in
terms of global indices, the ticks are drawn at -0.3/5, 1/5, 1.5/5, etc).
The first set of ticks are drawn at every half integer. The second set of
ticks are labelled with global indices. The :class:`Tickline` is horizontal,
and runs from right to left. The tick*line* is centered in the middle of the
widget, and the :class:`DataListTick` sit on top of the line.

In addition to the attributes introduced above, :attr:`Tickline.min_index`,
:attr:`Tickline.max_index`, :attr:`Tickline.min_scale`, and 
:attr:`Tickline.max_scale` can be used to limit the sections of the Tickline
that can be shown, and how much can be zoomed in or out.

Customizations
--------------

There are 4 recommended extension points with regard to :class:`Tick` and
:class:`Tickline` in order of least to most change:
:meth:`Tick.draw`, :meth:`Tick.tick_iter`, :meth:`Tick.display`, and 
:meth:`Tickline.redraw_`. These 4 methods form the gist of redrawing operation.
In simple terms, :meth:`Tickline.redraw_` calls :meth:`Tick.display` for each
tick in :attr:`Tickline.ticks`. ``display`` then calls :meth:`Tick.tick_iter`
to obtain an iterator of relevant information regarding the list of ticks
that should be shown, and hands off each individual info to :meth:`Tick.draw`
to compute the graphics. 

A possible extension is to draw triangle ticks instead
of rectangles. In this case, overriding :meth:`Tick.draw` is most appropriate.
Another extension can be drawing a timeline, in which case 
:meth:`Tick.tick_iter` may be overriden to produce information about  
datetimes instead of plain global indices for ease of logic handling.

:class:`Tick`'s underlying drawing utilizes Mesh to ensure smooth graphics,
but this may not be appropriate for certain visuals. To change this behavior,
overriding :meth:`Tick.display` can be appropriate. 

Finally, if major changes to how :class:`Tickline` works are necessary,
override :meth:`Tickline.redraw_`. However, for most cases, it is recommended
to customize a version of *tick labeller*, which can be a subclass or
a ducktype of :class:`TickLabeller`. This is an object that handles
labelling and/or custom graphics for the tickline. The tick labeller can
be specified by passing a class to :attr:`Tickline.labeller_cls`; any
initialization keyword arguments should be passed as a dict to
:attr:`Tickline.labeller_args`. See the class documentation
of :class:`TickLabeller` for more details.

Graphics
========

.. versionchanged:: 0.1.1

    A custom background image maybe inserted as BorderImage by giving
    :attr:`Tickline.background_image` the path to the image.
    :attr:`Tickling.border` adjusts the borders parameter to the BorderImage.
    
    By default, there's no background image, but a Rectangle with 
    :attr:`Tickline.background_color` covers the background. This can be
    turned off via :attr:`Tickline.cover_background`.

Hack it!
--------

The technology behind :class:`Tickline` is actually quite versatile, and
it's possible to use it to build seemingly unrelated things. For example,
a selection wheel like in iOS has been created by subclassing it.
'''

__version__ = '0.1.1'

from bisect import bisect_left, bisect
from kivy.clock import Clock
from kivy.core.text import Label as CoreLabel
from kivy.effects.dampedscroll import DampedScrollEffect
from kivy.graphics import InstructionGroup, Mesh
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle, Line
from kivy.metrics import dp, sp
from kivy.properties import ListProperty, NumericProperty, OptionProperty, \
    ObjectProperty, BoundedNumericProperty, BooleanProperty, AliasProperty, \
    DictProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.stencilview import StencilView
from kivy.uix.widget import Widget
from kivy.vector import Vector
from math import ceil, floor
from kivy.graphics.vertex_instructions import BorderImage

class TickLabeller(Widget):
    '''handles labelling and/or custom graphics for a :class:`Tickline`. 
    
    Often, when there are multiple :class:`Tick`s drawn on a :class:`Tickline`,
    labelling can become messy. For example, if a major tick coincides with
    a minor tick, without some customization of display logic, the major
    label will sit on top of the minor label. The :class:`TickLabeller` is
    designed to centralize tick information and elegantly handle labelling
    and/or custom graphics.
    
    Its work cycle corresponds to each :meth:`~Tickline.redraw`. 
    
    At the start of redraw, the method :meth:`re_init` is called. This should 
    set up the :class:`TickLabeller` for a new round of labelling. 
    
    During the redraw, ticks that need to be labelled should called 
    :meth:`register` to register the relevant information for rendering
    a label.
    
    Finally, at the end of redraw, :class:`Tickline` calls :meth:`make_labels`
    to produce the labels. Note that it is not required to reproduce labels
    in :meth:`make_labels` at every run, or to delay the production of labels
    to :meth:`make_labels` --- it is entirely possible to label on demand
    in :meth:`register`. 
    
    As a generic labeller, :class:`TickLabeller` only seeks to prevent 
    overlapping labels. It still relies on the :class:`Tick`s to produce
    the actual label texture through :meth:`Tick.get_label_texture`.
    
    A class can inherit from this or just ducktype to be used similarly
    with :class:`Tickline` and :class:`Tick`.'''
    
    def __init__(self, tickline, **kw):
        super(TickLabeller, self).__init__(**kw)
        self.tickline = tickline
        self.registrar = {}
        
    def re_init(self, *args):
        '''method for reinitializing and accept registrations from a new
        redraw. Override if necessary.'''
        self.registrar = {}
        
    def register(self, tick, tick_index, tick_info):  
        tick_sc = tick.scale(self.tickline.scale)
        tickline = self.tickline
        texture = tick.get_label_texture(tick_index)
        if texture and tick_sc > tick.min_label_space:
            if tickline.is_vertical():
                x, tick_pos = (tick_info[0],
                               tick_info[1] + tick_info[3] / 2)
                align = tick.halign
                if align in ('left', 'line_right'):
                    l_x = x + tick.tick_size[1] + tickline.tick_label_padding
                else:
                    l_x = x - texture.width - tickline.tick_label_padding
                pos = (l_x, tick_pos - texture.height / 2)
            else:
                tick_pos, y = (tick_info[0] + tick_info[2] / 2,
                               tick_info[1])
                align = tick.valign
                if align in ('top', 'line_bottom'):
                    l_y = y - texture.height - tickline.tick_label_padding
                else:
                    l_y = y + tick.tick_size[1] + tickline.tick_label_padding
                pos = (tick_pos - texture.width / 2, l_y)
            if (tick_pos, align) not in self.registrar or \
                self.registrar[(tick_pos, align)][1] > tick.scale_factor:
                self.registrar[(tick_pos, align)] = (texture, pos,
                                                     tick.scale_factor)
    def make_labels(self):
        canvas = self.tickline.canvas
        group_id = self.group_id
        canvas.remove_group(group_id)
        with canvas:
            for texture, pos, _ in self.registrar.values():
                Rectangle(texture=texture, pos=pos,
                          size=texture.size,
                          group=group_id)
    @property
    def group_id(self):
        return self.__class__.__name__
    
class CompositeLabeller(TickLabeller):
    '''combines multiple labellers into one. 
    
    Initialize with an instance of :class:`Tickline` and a dictionary 
    containing information regarding what labeller should handle what kind
    of ticks. Specifically, the dict should be keyed by labeller *classes*,
    and the values should be a list of subclasses of 
    :class:`Tick` assigned to be handled by the corresponding labeller. 
    For example, ``{TickLabeller: [Tick], OtherLabeller: [DataListTick]}``
    would be a valid dict.
    
    .. note::
        The labellers will on handle ticks of *exactly* those types 
        specified, i.e. NOT their subtypes as well.
    
    In addition, the last element of each list may be a dict of keyword
    arguments to be passed to the corresponding tick labeller. For example::
    
        CompositeLabeller(some_tickline, 
                        {TickLabeller: [Tick], 
                         TimeLabeller: [TimeTick, {'date_halign': 'right'}]
                         })
                         
    would instantiate the ``TimeLabeller`` as 
    ``TimeLabeller(some_tickline, date_halign='right')``.
    '''
    def __init__(self, tickline, labellers):
        self.tickline = tickline
        self.init_designater(labellers)
        
    def re_init(self, *args):
        for labeller in self.labellers:
            labeller.re_init(*args)
            
    def init_designater(self, labellers):
        self.designater = {}
        self.labellers = []
        for labeller_cls, tick_types in labellers.items():
            if isinstance(tick_types[-1], dict):
                labeller = labeller_cls(self.tickline, **tick_types[-1])
                tick_types.pop()
            else:
                labeller = labeller_cls(self.tickline)
            self.labellers.append(labeller)
            for tp in tick_types:
                self.designater[tp] = labeller
                
    def register(self, tick, *args, **kw):
        labeller = self.designater[type(tick)]
        labeller.register(tick, *args, **kw)
        
    def make_labels(self):
        for labeller in self.labellers:
            labeller.make_labels()
        
class Tickline(StencilView):
    '''See module documentation for details.'''
    #===========================================================================
    # visual attributes
    #===========================================================================
    '''most of the following properties are in place for quick usage.
    For more involved graphics customization, design a :class:`TickLabeller`.'''
    
    background_color = ListProperty([0, 0, 0])
    '''color in RGB of the background.'''

    cover_background = BooleanProperty(True)
    '''controls whether to draw a Rectangle covering the background,
    underneath :attr:`background_image`, if any.
    
    .. versionadded:: 0.1.1
    '''
    
    backward = BooleanProperty(False)
    '''By default, the Tickline runs left to right if :attr:`orientation`
    is 'horizontal' and bottom to top if it's 'vertical'. If :attr:`backward`
    is true, then this is reversed.'''

    def get_dir(self):
        return -1 if self.backward else 1
    def set_dir(self, val):
        self.backward = True if val <= 0 else False
    dir = AliasProperty(get_dir, set_dir, bind=['backward'])
    '''gives -1 if :attr:`backward` is true, otherwise 1.'''
    
    orientation = OptionProperty('vertical', options=['horizontal', 'vertical'])
    '''orientation of the :class:`Tickline`. Can be either 'horizontal' or
    'vertical'. Defaults to 'vertical'.'''

    draw_line = BooleanProperty(True)
    '''a toggle for whether the center line is drawn or not.'''

    line_color = ListProperty([1, 1, 1, 1])
    '''color of the tick*line*.'''
    
    line_width = NumericProperty(4.)
    '''width of the tick*line*.'''
    
    line_offset = NumericProperty(0)
    '''how far the tick*line* should deviate from the center.'''

    def get_line_pos(self):
        if self.is_vertical():
            return self.center_x + self.line_offset
        else:
            return self.center_y + self.line_offset
    def set_line_pos(self, val):
        if self.is_vertical():
            self.line_offset = val - self.center_x
        else:
            self.line_offset = val - self.center_y
    line_pos = AliasProperty(get_line_pos, set_line_pos,
                             bind=['orientation', 'line_offset',
                                   'center_x', 'center_y'])
    '''the absolute position of the tick*line* on screen, if :attr:`draw_line`
    is True'''

    tick_label_padding = NumericProperty(9)
    '''the padding between a tick and its label.'''

    labeller_cls = ObjectProperty(TickLabeller)
    '''the class used to handle labelling. Defaults to :class:`TickLabeller`'''

    labeller_args = DictProperty()
    '''a dictionary of keyword arguments to be passed into the
    :attr:`labeller_cls` construtor.'''
    
    labeller = ObjectProperty(None)
    '''an instance of :attr:`labeller_cls` used for labelling and
    custom graphics.'''

    background_image = StringProperty(None, allownone=True)
    '''background image to have below all graphics renderings. This is
    rendered as a BorderImage.,
    
    .. versionadded:: 0.1.1
    '''
    
    border = ListProperty([16, 16, 16, 16])
    '''specifies the borders of the background image to feed into BorderImage.
    
    .. versionadded:: 0.1.1
    '''
    #===========================================================================
    # touch
    #===========================================================================
    ticks = ListProperty()    
    '''a list of :class:`Tick` objects to draw'''

    zoomable = BooleanProperty(True)
    '''a toggle for whether this :class:`Tickline` can be zoomed in and out.'''
    
    translation_touches = BoundedNumericProperty(1, min=1)
    '''decides whether translation is triggered by a single touch 
    or multiple touches.'''

    drag_threshold = NumericProperty('20sp')
    '''the threshold to determine whether a touch constitutes a scroll.'''
    
    scroll_effect_cls = ObjectProperty(DampedScrollEffect)

    scroll_effect = ObjectProperty(None, allownone=True)
    ''':attr:`scroll_effect`.value should always point toward :attr:`index_mid`.
    '''

    #===========================================================================
    # other public attributes
    #===========================================================================
    
    min_index = NumericProperty(-float('inf'))
    '''The minimal value :attr:`index_mid` can assume. Defaults to -inf,
    meaning the absence of such a minimum.'''
    
    max_index = NumericProperty(float('inf'))
    '''The maximal value :attr:`index_mid` can assume. Defaults to inf,
    meaning the absence of such a maximum.'''

    index_0 = NumericProperty(0) 
    '''gives the index, likely fractional, that corresponds to 
    ``self.x`` if :attr:`orientation` is 'vertical', or ``self.y``
    if :attr:`orientation` is 'horizontal'. Note that this doesn't 
    depend on :attr:`Tickline.backward`.'''    
    
    index_1 = NumericProperty(10)
    '''gives the index, likely fractional, that corresponds to 
    ``self.right`` if :attr:`orientation` is 'vertical', or ``self.top``
    if :attr:`orientation` is 'horizontal'. Note that this doesn't 
    depend on :attr:`Tickline.backward`.'''    
 
    def get_index_mid(self):
        return (self.index_0 + self.index_1) / 2.
    def set_index_mid(self, val):
        half_length = self.line_length / 2. / self.scale
        self.index_0 = val - half_length
        self.index_1 = val + half_length
    index_mid = AliasProperty(get_index_mid, set_index_mid,
                              bind=['index_0', 'index_1'])
    '''returns the index corresponding to the middle of the tickline.
    Setting this attribute as the effect of translating the tickline.
    '''
    
    def get_line_length(self):
        return self.size[1 if self.is_vertical() else 0]  
    def set_line_length(self, val):
        if self.is_vertical():
            self.size[1] = val
        else:
            self.size[0] = val
    line_length = AliasProperty(get_line_length, set_line_length, cache=True,
                            bind=['size', 'orientation'])
    '''returns the length of the :class:`Tickline` widget along the direction
    it extends.'''
    
    def get_pos0(self):
        return self.y if self.is_vertical() else self.x
    def set_pos0(self, val):
        if self.is_vertical():
            self.y = val
        else:
            self.x = val
    pos0 = AliasProperty(get_pos0, set_pos0,
                         bind=['size', 'x', 'y', 'orientation'])
    '''the coordinate of Tickline that's along the direction it extends.'''
    
    def get_scale_min(self, *args):
        if self._scale_min is not None:
            return self._scale_min
        return self._get_scale_min()
    def _get_scale_min(self, *args):
        if not self.ticks:
            return 0
        return min(tick.min_space * tick.scale_factor
                   for tick in self.ticks)
    def set_scale_min(self, val):
        self._scale_min = val
    scale_min = AliasProperty(get_scale_min, set_scale_min,
                              bind=['_scale_min', 'ticks'])
    '''minimal bound on :attr:`scale`, 
    specifying the max that one can zoom *out*. If None, then one can
    zoom out as long as the widest set of ticks has more than its 
    :attr:`~Tick.min_space`.'''
    

    def get_scale_max(self, *args):
        if self._scale_max is not None:
            return self._scale_max
        return self._get_scale_max()
    def _get_scale_max(self, *args):
        if not self.ticks:
            return float('inf')
        return max(self.line_length * tick.scale_factor
                   for tick in self.ticks)        
    def set_scale_max(self, val):
        self._scale_max = val
    scale_max = AliasProperty(get_scale_max, set_scale_max,
                              bind=['_scale_max', 'line_length', 'scale', 'ticks'])
    '''maximal bound on :attr:`scale`,
    specifying the max that one can zoom *in*. If None, then one can zoom in
    as long as the narrowest set of ticks has spacing no greater than this
    Tickline's width (if it's horizontal) or height (if it's vertical).'''

    densest_tick = ObjectProperty(None)
    '''represents the smallest interval shown on screen.'''
    
    in_motion = BooleanProperty(False)
    '''gives False if and only if the :class:`Tickline` is moving.'''

    def get_scale(self):
        if self._versioned_scale is not None:
            scale = self._versioned_scale
            self._versioned_scale = None
            return scale
        try:
            return self.line_length / (self.index_1 - self.index_0) * self.dir 
        except ZeroDivisionError:
            return float('inf')
    def set_scale(self, val):
        self.index_1 = self.index_0 + self.dir * self.line_length / val
    scale = AliasProperty(get_scale, set_scale,
                          bind=['index_0', 'index_1', 'line_length', 'dir'])
    '''the distance between 2 ticks of consecutive *global index*.'''
    
    redraw = ObjectProperty(None)
    '''a trigger to redraw graphics. In most cases this is not necessary
    to call publicly as it is already bound to relevant properties.
    The actual redrawing is done by :meth:`redraw_`.'''
    #===========================================================================
    # private attributes
    #===========================================================================
    
    scale_tolerances = ListProperty()
    '''essentially::
    
        sorted([(tick.scale_factor * tick.min_space, tick) for tick in self.ticks])
        
    This is used to determine :attr:`densest_tick`'''
    
    line_instr = ObjectProperty(None)
    '''instruction for drawing the *line*.'''
    
    line_color_instr = ObjectProperty(None)
    '''instruction for line color.'''
    
    _versioned_scale = NumericProperty(None, allownone=True)
    '''(internal) used to suppress :attr:`scale` change during a translation.'''
   
    _scale_min = NumericProperty(None, allownone=True) 
    _scale_max = NumericProperty(None, allownone=True)
    #===========================================================================
    # methods 
    #===========================================================================
    def __init__(self, *args, **kw):
        self._trigger_calibrate = \
                    Clock.create_trigger(self.calibrate_scroll_effect, -1)
        self.redraw = _redraw_trigger = \
                                Clock.create_trigger(self.redraw_, -1)
        super(Tickline, self).__init__(*args, **kw)
        self._touches = []
        self._last_touch_pos = {}
        self.scroll_effect = self.scroll_effect_cls()
        self.on_scroll_effect_cls()
        self.bind(index_0=_redraw_trigger,
                  index_1=_redraw_trigger,
                  pos=_redraw_trigger,
                  size=_redraw_trigger,
                  orientation=_redraw_trigger,
                  ticks=_redraw_trigger)
        self.bind(index_mid=self._trigger_calibrate)
        self.init_center_line_instruction()
        self.init_background_instruction()
        self.on_ticks()
        self._update_densest_tick()
        self.labeller = self.labeller_cls(self, **self.labeller_args)

    def on_scale(self, *args):
        self._update_densest_tick()
        self._update_effect_constants()
        self.redraw()
        
    def on_backward(self, *args):
        if self.index_0 < self.index_1 and self.backward:
            self.index_0, self.index_1 = self.index_1, self.index_0
            
    def on_ticks(self, *args):
        self._update_tolerances()
        for tick in self.ticks:
            tick.bind(scale_factor=self._update_tolerances,
                      min_space=self._update_tolerances)
        canvas = self.canvas
        if not canvas:
            return
        canvas.clear()
        canvas.add(self.background_instr)
        if self.draw_line:
            canvas.add(self.line_color_instr)
            canvas.add(self.line_instr)
        for tick in self.ticks:
            canvas.add(tick.instr)           
    
    def on_labeller_cls(self, *args):        
        self.labeller = self.labeller_cls(self, **self.labeller_args)
        
    def on_labeller_args(self, *args):        
        self.labeller = self.labeller_cls(self, **self.labeller_args)
        
    def on_scroll_effect_cls(self, *args):
        effect = self.scroll_effect = self.scroll_effect_cls(round_value=False)
        self._update_effect_constants()
        self._trigger_calibrate()
        effect.bind(scroll=self._update_from_scroll)
        effect.bind(velocity=self.update_motion,
                    is_manual=self.update_motion)
        
    def on_pos(self, *args):
        self.redraw()
        self._trigger_calibrate()
        
    def on_max_index(self, *args):
        try:
            self._trigger_calibrate()
        except AttributeError:
            return
        
    def on_min_index(self, *args):
        try:
            self._trigger_calibrate()
        except AttributeError:
            return       
        
    def on_line_color(self, *args):
        self.line_color_instr.rgba = self.line_color

    def update_motion(self, *args):
        effect = self.scroll_effect
        self.in_motion = effect.velocity or effect.is_manual
    
        
    def translate_by(self, distance):
        self._versioned_scale = self.scale
        self.index_0 += distance
        self.index_1 += distance


    def calibrate_scroll_effect(self, *args, **kw):
        if not self.scroll_effect:
            return
        effect = self.scroll_effect
        effect.min = self.min_index 
        effect.max = self.max_index
        effect.value = self.index_mid
        return True
        
    def pos2index(self, pos, window=False):
        '''converts a position coordinate along the tickline direction to its
        index. If ``window`` is given as True, then the coordinate is assumed
        to be a window coordinate.'''
        return self.index_0 + \
            self.dir * float(pos - window * self.pos0) / self.scale 
        
    def index2pos(self, index, i0=None, i1=None, i_mid=None):
        '''returns the position of a index (the global index, not a localized
        tick index), even if out of screen, based on the current :attr:`index_0`
        , :attr:`index_1`, and :attr:`line_length`. Optionally, ``i0`` and/or
        ``i1`` can be given to replace respectively :attr:`index_0` and
        :attr:`index_1` in the calculation.
        
        .. note::
            the absolute position (relative to the window) is given.
            
        :param index: index to be converted to pos
        :param i0: the ``index_0`` corresponding to the situation in which
            we want to translate ``index`` to a position. By default we
            use :attr:`index_0`.
        :param i1: the ``index_1`` corresponding to the situation in which
            we want to translate ``index`` to a position. By default we
            use :attr:`index_1`.
        :param i_mid: The middle index, halfway between ``i0`` and ``i1``.
            If this is given, then ``i0`` and ``i1`` are calculated from 
            ``i_mid`` using the current :attr:`scale`.
         ''' 
        if i_mid is not None:
            i0 = i_mid - float(self.line_length) / 2 / self.scale * self.dir
            i1 = i_mid + float(self.line_length) / 2 / self.scale * self.dir
        else:
            i0, i1 = i0 or self.index_0, i1 or self.index_1
        return float(i0 - index) / (i0 - i1) * self.line_length + self.pos0
        
    def calc_intercept(self, anchor, antianchor, to_window=False): 
        '''given 2 points ``anchor`` and ``antianchor`` (that usually
        represent 2 touches), 
        find the point on the Tickline that should be fixed through out
        a scatter operation.
        
        If ``to_window`` is given as True, the resulting coordinate is
        returned as a window coordinate. Otherwise, by default, the coordinate
        returned is with respect to this widget.
        
        .. note::
            ``anchor`` and ``antianchor`` are assumed to have window coordinates.
        '''
        
        if self.is_vertical():
            return (anchor.y + antianchor.y) / 2 - (1 - to_window) * self.pos0
        else:
            return (anchor.x + antianchor.x) / 2 - (1 - to_window) * self.pos0
    
    def is_vertical(self):
        return self.orientation == 'vertical'
    def init_center_line_instruction(self):
        if not self.draw_line:
            self.line_color_instr = self.line_instr = None
            return
        self.line_color_instr = Color(*self.line_color)
        if self.is_vertical():
            self.line_instr = Line(points=[self.line_pos,
                                           self.y,
                                           self.line_pos,
                                           self.top],
                                   width=self.line_width,
                                   cap='none')
        else:
            self.line_instr = Line(points=[self.x,
                                           self.line_pos,
                                           self.right,
                                           self.line_pos],
                                   width=self.line_width,
                                   cap='none')
        _update_line_pts = self._update_line_pts
        self.bind(orientation=_update_line_pts,
                  pos=_update_line_pts,
                  size=_update_line_pts,
                  draw_line=_update_line_pts)
    
    def init_background_instruction(self, *args):
        self.background_instr = instrg = InstructionGroup()
        instrg.add(Color(*self.background_color))
        if self.cover_background:
            instrg.add(Rectangle(pos=self.pos, size=self.size))
        if self.background_image is not None:
            instrg.add(BorderImage(source=self.background_image,
                                   size=self.size,
                                   pos=self.pos,
                                   border=self.border))
        update = self._update_background
        self.bind(background_color=update, pos=update, size=update,
                  background_image=update)
    def redraw_(self, *args):
        self.labeller.re_init()
        # draw ticks
        for tick in self.ticks:
            tick.display(self)
        # update labels
        self.labeller.make_labels()
    #===========================================================================
    # prive methods
    #===========================================================================
    def _update_tolerances(self, *args):
        self.scale_tolerances = sorted(
                               [(tick.scale_factor * tick.min_space, tick) 
                                for tick in self.ticks])
    
    def _update_effect_constants(self, *args):
        if not self.scroll_effect:
            return
        scale = self.scale
        effect = self.scroll_effect
        effect.drag_threshold = self.drag_threshold / scale
        effect.min_distance = .1 / scale
        effect.min_velocity = .1 / scale
        effect.min_overscroll = .5 / scale
        return True
    def _update_from_scroll(self, *args, **kw):
        # possible dispatch loop here: will have to watch for it in the future
        new_mid = self.scroll_effect.scroll
        shift = new_mid - self.index_mid
        self.translate_by(shift)

    def _update_line_pts(self, *args):
        if not self.line_instr:
            return
        if not self.draw_line:
            self.line_color_instr = self.line_instr = None
            return
        if self.is_vertical():
            self.line_instr.points = [self.line_pos,
                                      self.y,
                                      self.line_pos,
                                      self.top]
        else:
            self.line_instr.points = [self.x,
                                      self.line_pos,
                                      self.right,
                                      self.line_pos]
    def _update_background(self, *args):
        instrg = self.background_instr
        instrg.clear()
        instrg.add(Color(*self.background_color))
        if self.cover_background:
            instrg.add(Rectangle(pos=self.pos, size=self.size))
        if self.background_image is not None:
            instrg.add(BorderImage(source=self.background_image,
                                   size=self.size,
                                   pos=self.pos,
                                   border=self.border))
    def _update_densest_tick(self, *args):
        tol = self.scale_tolerances
        scale = self.scale
        i = bisect([t[0] for t in tol], scale)
        # tol[i-1] contains the tick with the largest scale_factor that can
        # still be displayed, or in other words, the tick with the smallest
        # interval
        try:
            self.densest_tick = tol[i - 1][1]
        except IndexError:
            self.densest_tick = None
            
    #===========================================================================
    # touch handling
    #===========================================================================
    def on_touch_down(self, touch):
        x, y = touch.x, touch.y
        
        if not self.collide_point(x, y):
            return False
        if super(Tickline, self).on_touch_down(touch):
            return True
        
        touch.grab(self)
        self._touches.append(touch)
        self._last_touch_pos[touch] = x, y
        if self.translate_now():
            self.scroll_effect.start(self.index_mid)
        else:
            self.scroll_effect.velocity = 0
            self.scroll_effect.cancel()
    def translate_now(self):
        return len(self._touches) == self.translation_touches
    def on_touch_move(self, touch):
        x, y = touch.x, touch.y
        collide = self.collide_point(x, y)
        
        if collide and not touch.grab_current == self:
            if super(Tickline, self).on_touch_move(touch):
                return True
        
        if touch in self._touches and touch.grab_current == self:
            self.transform_with_touch(touch)
            self._last_touch_pos[touch] = x, y
            
        if collide:
            return True
    def transform_with_touch(self, touch): 
        changed = False
        scale = self.scale
        
        if self.translate_now():
            if not self.is_vertical():
                d = touch.x - self._last_touch_pos[touch][0]
            else:
                d = touch.y - self._last_touch_pos[touch][1]

            d = d / self.translation_touches
            self.scroll_effect.update(self.index_mid - d / scale * self.dir)
            changed = True
            
        else:
            # no translation, so make sure cancel effects
            self.scroll_effect.velocity = 0
            self.scroll_effect.cancel()
            
        if len(self._touches) == 1 or not self.zoomable:
            return changed
        
        points = [Vector(self._last_touch_pos[t]) for t in self._touches]

        # we only want to transform if the touch is part of the two touches
        # furthest apart! So first we find anchor, the point to transform
        # around as the touch farthest away from touch
        anchor = max(points, key=lambda p: p.distance(touch.pos))

        # now we find the touch farthest away from anchor, if its not the
        # same as touch. Touch is not one of the two touches used to transform
        farthest = max(points, key=anchor.distance)
        if points.index(farthest) != self._touches.index(touch):
            return changed
        antianchor, pantianchor = Vector(*touch.pos), Vector(*touch.ppos)
        
        # the midpoint between the touches is to have the same index, while
        # all other points on the tickline are to scale away from this point.
        try:
            # note: these intercepts are local coordinates
            inter = self.calc_intercept(anchor, antianchor)
            old_inter = self.calc_intercept(anchor, pantianchor)
        except ZeroDivisionError:
            return False
        inter_index = self.pos2index(old_inter)
        scale_factor = ((antianchor - anchor).length() / 
                        (pantianchor - anchor).length())
        new_scale = scale_factor * scale
       
        if new_scale < self.scale_min:
            new_scale = self.scale_min
        elif new_scale > self.scale_max:
            new_scale = self.scale_max
            
        changed = inter != old_inter or new_scale != scale

        self.index_0 = index_0 = inter_index - self.dir * inter / new_scale
        self.index_1 = index_0 + self.dir * self.line_length / new_scale 
        # need to update the scroll effect history so that on touch up
        # it doesn't jump
        self.scroll_effect.update(self.index_mid)
        self.scroll_effect.is_manual = True
        changed = True
        return changed
    
    def on_touch_up(self, touch):
        x, y = touch.x, touch.y
        
        if not touch.grab_current == self:
            if super(Tickline, self).on_touch_up(touch):
                return True
        
        if touch in self._touches and touch.grab_state:
            if self.translate_now():
                self.scroll_effect.stop(self.index_mid)
            touch.ungrab(self)
            del self._last_touch_pos[touch]
            self._touches.remove(touch)
            
        if self.collide_point(x, y):
            return True
        
class Tick(Widget): 
    '''an object that holds information about a set of ticks to be drawn
    into a :class:`Tickline`.
    
    .. note::
        The graphics handling here is based on Mesh to enable quick drawing.
        for more complex_ graphics this may be overriden in a subclass,
        or use a custom TickLabeller to handle visuals.'''
    
    #===========================================================================
    # public attributes 
    #===========================================================================
    tick_size = ListProperty([dp(2), dp(8)])
    '''the first number always denotes the width (the shorter length).'''    
    
    halign = OptionProperty('left', options=['left', 'right',
                                              'line_left', 'line_right'])    
    '''if the :class:`Tickline` that draws this :class:`Tick` is
    vertical, then this attribute specifies where horizontally the 
    ticks are to be drawn. The options are "left", "right", "line_left",
    and "line_right". "line_left" draws the ticks on the left side of
    the tick*line*, while "line_right" draws the ticks on the right side of it.
    "left" and "right" respectively draws ticks on the left and right of
    the :class:`Tickline` widget.'''
    
    valign = OptionProperty('bottom', options=['top', 'bottom',
                                               'line_top', 'line_bottom'])
    '''if the :class:`Tickline` that draws this :class:`Tick` is
    horizontal, then this attribute specifies where vertically the 
    ticks are to be drawn. The options are "top", "bottom", "line_top",
    and "line_bottom". "line_top" draws the ticks on the top of
    the tick*line*, while "line_bottom" draws the ticks on the bottom of it.
    "top" and "bottom" respectively draws ticks on the top and bottom of
    the :class:`Tickline` widget.'''
    
    tick_color = ListProperty([1, 1, 1, 1])
    '''color of ticks drawn, specified as an rgba value.'''
    
    min_space = NumericProperty('10sp')
    '''if the spacing between consecutive ticks fall below this attribute,
    then this Tick will not be displayed.'''
    
    min_label_space = NumericProperty('37sp')
    '''if the spacing between consecutive ticks fall below this attribute,
    then this Tick's label will not be displayed.'''
    
    scale_factor = BoundedNumericProperty(1, min=1)
    '''The spacing of a Tick is determined by 
    :attr:`Tick.scale_factor` / :attr:`Tickline.scale`.'''
    
    offset = NumericProperty(0)
    '''causes :class:`Tick` to be draw at local indices 
    ``..., offset - 2, offset - 1, offset, offset + 1, offset + 2, ...``.
    
    This can be, for example, used to display day ticks in a 
    timezone aware manner.
    '''
    
    label_global = BooleanProperty(False)
    '''If True, the default labelling of this Tick is of the global index.
    Otherwise, the default labelling is the local (integer) index. The 
    "default labelling" here refers to the usage of :class:`TickLabeller`
    to handle labelling. Custom tick labellers may ignore this setting.
    
    :attr:`label_global` defaults to False.'''
    
    #===========================================================================
    # private attributes
    #===========================================================================
    
    _mesh = ObjectProperty(None)
    '''The Mesh instruction that is used to draw ticks.'''
    
    instr = ObjectProperty(None)
    '''The instruction group used to draw ticks in addition to any other
    customizations.'''
    
    def __init__ (self, *args, **kw):
        self._mesh = Mesh(mode='triangle_strip')
        self._color = Color(*self.tick_color)
        self.instr = instr = InstructionGroup()
        instr.add(self._color)
        instr.add(self._mesh)
        super(Tick, self).__init__(*args, **kw)

    def on_tick_color(self, *args):
        self._color.rgba = self.tick_color

    def scale(self, sc):
        '''returns the spacing between ticks, given the global scale of 
        a :class:`Tickline`.
        
        :param sc: the :attr:`~Tickline.scale` of the :class:`Tickline` 
            this Tick belongs to'''
        return float(sc) / float(self.scale_factor)
    
    def unscale(self, tick_sc):
        '''reverse of :meth:`scale`.
        
        :param tick_sc: the scale of this Tick to be scaled back to the global
            scale of the :class:`Tickline` this Tick belongs to.
        '''
        return float(tick_sc) * float(self.scale_factor)
    
    def localize(self, index):
        '''turn a global index of :class:`Tickline` to the index used by
        this Tick.
        
        :param index: a global index of the :class:`Tickline` this Tick
            belongs to.
        '''
        return index * self.scale_factor
    
    
    def get_label_texture(self, index, **kw):
        '''
        Return a label *texture* for a tick given its ordinal position. 
        Return None if there shouldn't be a label at ``index``. This method
        should optimized for quickly drawing labels on screen.
        
        :param index: the ordinal number of a tick from the 0th tick, 
            which is the tick that would have global index 0
            if it were the first visible tick.
        :param kw: keyword args passed to Label
        '''        
        kw['font_size'] = self.tick_size[1] * 2
        label = CoreLabel(
            text=str(index / (self.label_global and self.scale_factor or 1)),
            **kw)
        label.refresh()
        return label.texture
    
    def extended_index_0(self, tickline):
        d_tick = tickline.densest_tick
        localize = d_tick.localize
        globalize = d_tick.globalize
        
        return globalize(localize(tickline.index_0) + tickline.backward)
    
    def extended_index_1(self, tickline):
        d_tick = tickline.densest_tick
        localize = d_tick.localize
        globalize = d_tick.globalize
        
        return globalize(localize(tickline.index_1) - tickline.backward)
    
        
    def tick_iter(self, tickline):
        '''generates tick information for graphing and labeling in an iterator.
        By default, calls :meth:`tick_pos_index_iter` to return a pair 
        consisting of the position on screen and the localized tick index
        of the tick to be drawn.
        
        ..note::
            In general, the iterator should generate all the tick information
            for ticks to be drawn on screen. This in most cases would also
            include ticks just out of screen, but needs to be drawn partially.
        '''
        return self.tick_pos_index_iter(tickline)
    
    def tick_pos_index_iter(self, tl):
        '''given the parent :class:`Tickline` of this Tick, return an iterator
        of the positions and (localized) indices that correspond to ticks
        that should be drawn.
        
        :param tl: :class:`Tickline` that this Tick belongs to.
        '''
        
        tick_index, tick_pos, tick_sc = \
            self._get_index_n_pos_n_scale(tl, True)
        if tick_sc < self.min_space:
            raise StopIteration
        condition = self._index_condition(tl, True)
        pos0 = tl.y if tl.is_vertical() else tl.x
        while condition(tick_index):
            yield tick_pos + pos0, tick_index
            tick_pos += tick_sc
            tick_index += tl.dir    
        raise StopIteration
    
    def display(self, tickline):
        '''main method for displaying Ticks. This is called after every
        scatter transform. Uses :attr:`draw` to handle actual drawing.
        '''
        mesh = self._mesh
        self._vertices = []
        for tick_info in self.tick_iter(tickline):
            self.draw(tickline, tick_info)
        indices = list(range(len(self._vertices) // 4))
        mesh.vertices = self._vertices  
        mesh.indices = indices
        
    def draw(self, tickline, tick_info):
        '''Given information about a tick, present in on screen. May be 
        overriden to provide customized graphical representations, for 
        example, to graph a set of points.
        Uses :attr:`Tickline.labeller` to handle labelling.
        
        :param tickline: a :class:`Tickline` instance.
        :param tick_info: an object holding information about the tick to be
            drawn. By default, it's a pair holding the position and the index
            of the tick. Should be overriden as necessary. 
        '''        
        tick_pos, tick_index = tick_info
        tick_rect = self.draw_tick(tickline, tick_pos)
        tickline.labeller.register(self, tick_index, tick_rect)
        
    
    def globalize(self, tick_index):
        '''convert a index of this Tick to the global index used in the
        :class:`Tickline` this Tick belongs to. Note that the returned value
        is a float, since most likely ``tick_index`` refers to a fractional 
        tick.
        :param tick_index: the index of this Tick to be converted
        '''
        return float(tick_index) / self.scale_factor
    
    def draw_tick(self, tickline, tick_pos, return_only=False):
        tw, th = self.tick_size
        if tickline.is_vertical():
            halign = self.halign
            if halign == 'left':
                x = tickline.x
            elif halign == 'line_left':
                x = tickline.line_pos - th
            elif halign == 'line_right':
                x = tickline.line_pos
            else:
                x = tickline.right - th
            y = tick_pos - tw / 2
            height, width = tw, th
            if not return_only:
                self._vertices.extend([x, y, 0, 0,
                                       x, y + height, 0, 0,
                                       x + width, y + height, 0, 0,
                                       x + width, y, 0, 0,
                                       x, y, 0, 0,
                                       x, y + height, 0, 0])
        else:
            valign = self.valign
            if valign == 'top':
                y = tickline.top - th
            elif valign == 'line_top':
                y = tickline.line_pos
            elif valign == 'line_bottom':
                y = tickline.line_pos - th
            else:
                y = tickline.y
            x = tick_pos - tw / 2
            width, height = tw, th
            if not return_only:
                self._vertices.extend([x, y, 0, 0,
                                       x + width, y, 0, 0,
                                       x + width, y + height, 0, 0,
                                       x, y + height, 0, 0,
                                       x, y, 0, 0,
                                       x + width, y, 0, 0,])
        return (x, y, width, height)
    #===========================================================================
    # private methods
    #===========================================================================
    def _get_index_n_pos_n_scale(self, tickline, extended=False):    
        ''' utility function for getting the first tick index and position
         at the bottom of the screen, along with the localized scale of the Tick.
         
         If ``extended``, gives index and position for a tick just below the 
         screen, as determined by :attr:`Tickline.densest_tick`.
         
         :param tickline: a :class:`Tickline` instance, usually the one this
             Tick draws on.
         :param extended: flag for giving tick information for just below
             the display area. Defaults to False
         '''
        tick_sc = self.scale(tickline.scale)
        if extended:
            index_0 = self.extended_index_0(tickline)
        else:
            index_0 = tickline.index_0 
        tick_index_0 = index_0 * self.scale_factor
        trunc = floor if tickline.backward else ceil
        tick_index = trunc(tick_index_0 - tickline.dir * self.offset) + \
                        tickline.dir * self.offset
        tick_pos = (self.globalize(tick_index) - tickline.index_0) * \
                    tickline.scale * tickline.dir
        return tick_index, tick_pos, tick_sc
    def _index_condition(self, tickline, extended=False):
        '''If ``extended``, 
        returns a boolean functional that returns True iff the input is a
        localized tick index within the range displayable on screen, or just
        one above or below.
        
        Otherwise, the returned functional returns True iff the input is 
        strictly on screen'''
        
        if extended:
            index_0 = self.extended_index_0(tickline)
            index_1 = self.extended_index_1(tickline)        
        else:
            index_0 = tickline.index_0
            index_1 = tickline.index_1        
        localize = self.localize
        index_0 = localize(index_0)
        index_1 = localize(index_1)
        if tickline.backward:
            return lambda idx: index_1 <= idx <= index_0
        else:
            return lambda idx: index_0 <= idx <= index_1        
    
class LabellessTick(Tick):
    '''same thing as :class:`Tick`, except no labels. Commonly used as
    the finest set of ticks.'''

    def get_label_texture(self, *args, **kw):
        return None
    
class DataListTick(Tick):
    '''takes a sorted list of tick indices and displays ticks at those marks.
    
    Note that because likely the tick indices will not be at regular intervals,
    :attr:`min_label_space` is set to 0 by default. Adjust it to your own 
    liking.'''

    data = ListProperty([])
    '''assumed to be sorted least to greatest; otherwise tick drawing
    might not work'''
    min_label_space = NumericProperty(0)
    halign = OptionProperty('line_right', options=Tick.halign.options)
    
    def tick_pos_index_iter(self, tl):
        index_0 = self.localize(self.extended_index_0(tl))
        index_1 = self.localize(self.extended_index_1(tl))
        tick_sc = self.scale(tl.scale)
        if tick_sc < self.min_space:
            raise StopIteration
            
        try:
            data_index = bisect_left(self.data, index_1 if tl.backward 
                                                            else index_0)
            tick_index = self.data[data_index]
            condition = self._index_condition(tl, True)
            while condition(tick_index):
                yield (tl.index2pos(self.globalize(tick_index)),
                       tick_index)
                data_index += 1
                tick_index = self.data[data_index]
        except IndexError:
            raise StopIteration
        
    
if __name__ == '__main__':
    from kivy.base import runTouchApp
    from kivy.uix.accordion import Accordion, AccordionItem
    acc = Accordion(orientation='vertical')
    complex_ = AccordionItem(title='complex_tickline')
    complex_.add_widget(Tickline(ticks=[Tick(tick_size=[4, 20], offset=.5),
                                    Tick(scale_factor=5., label_global=True),
                                    LabellessTick(tick_size=[1, 4],
                                         scale_factor=25.),
                                    DataListTick(data=[-0.3, 1, 1.5,
                                                       2, 4, 8, 16, 23],
                                                 scale_factor=5.,
                                                 halign='line_right',
                                                 valign='line_top')
                                    ],
                             orientation='horizontal',
                             backward=True,
                             min_index=0,
                             max_index=10))
    acc.add_widget(complex_)
    simple = AccordionItem(title='simple_tickline')
    simple.add_widget(Tickline(ticks=[Tick()]))
    acc.add_widget(simple)
    b = BoxLayout(padding=[10, 10, 10, 10], orientation='vertical')
    b.add_widget(acc)
    runTouchApp(b)
