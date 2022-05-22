conky.config = {

    --Various settings

    background = true,                          -- forked to background
    cpu_avg_samples = 2,                        -- The number of samples to average for CPU monitoring.
    diskio_avg_samples = 10,                    -- The number of samples to average for disk I/O monitoring.
    double_buffer = true,                       -- Use the Xdbe extension? (eliminates flicker)
    if_up_strictness = 'address',               -- how strict if testing interface is up - up, link or address
    net_avg_samples = 2,                        -- The number of samples to average for net data
    no_buffers = true,                          -- Subtract (file system) buffers from used memory?
    temperature_unit = 'celsius',               -- fahrenheit or celsius
    text_buffer_size = 2048,                    -- size of buffer for display of content of large variables - default 256
    update_interval = 30,                        -- update interval
    imlib_cache_size = 0,                       -- disable image cache to get a new spotify cover per song


    --Placement

    -- alignment = 'top_right',                  -- top-left,top-middle,top-right,bottom-left,bottom-middle,bottom-right,
                                                -- middle-left,middle-middle,middle-right,none
    alignment = 'top_right',
    --Arch Duoscreen
    --gap_x = -1910,
    gap_x = 100,                                 -- pixels between right or left border
    gap_y = 120,                                 -- pixels between bottom or left border
    maximum_height = 100,                       -- minimum height of window
    maximum_width = 620,                        -- maximum width of window

    --Graphical

    border_inner_margin = 5,                    -- margin between border and text
    border_outer_margin = 5,                    -- margin between border and edge of window
    border_width = 0,                           -- border width in pixels
    default_bar_width = 280,                    -- default is 0 - full width
    default_bar_height = 10,                    -- default is 6
    default_gauge_height = 25,                  -- default is 25
    default_gauge_width =40,                    -- default is 40
    default_graph_height = 40,                  -- default is 25
    default_graph_width = 153,                  -- default is 0 - full width
    default_shade_color = '#000000',            -- default shading colour
    default_outline_color = '#000000',          -- default outline colour
    draw_borders = false,                       -- draw borders around text
    draw_graph_borders = true,                  -- draw borders around graphs
    draw_shades = false,                        -- draw shades
    draw_outline = false,                       -- draw outline
    stippled_borders = 0,                       -- dashing the border

    --Textual

    extra_newline = false,                      -- extra newline at the end - for asesome's wiboxes
    format_human_readable = true,               -- KiB, MiB rather then number of bytes
    font = 'Noto Mono:size=11:regular',             -- font for complete conky unless in code defined
    max_text_width = 0,                         -- 0 will make sure line does not get broken if width too smal
    max_user_text = 16384,                      -- max text in conky default 16384
    override_utf8_locale = true,                -- force UTF8 requires xft
    short_units = true,                         -- shorten units from KiB to k
    top_name_width = 21,                        -- width for $top name value default 15
    top_name_verbose = false,                   -- If true, top name shows the full command line of  each  process - Default value is false.
    uppercase = false,                          -- uppercase or not
    use_spacer = 'none',                        -- adds spaces around certain objects to align - default none
    use_xft = true,                             -- xft font - anti-aliased font
    xftalpha = 1,                               -- alpha of the xft font - between 0-1

    --Windows

    own_window = true,                          -- create your own window to draw
    own_window_argb_value = 0,                 -- real transparency - composite manager required 0-255
    own_window_argb_visual = true,              -- use ARGB - composite manager required
    own_window_class = 'Conky',                 -- manually set the WM_CLASS name for use with xprop
    own_window_colour = '#000000',              -- set colour if own_window_transparent no
    own_window_hints = 'undecorated,below,above,sticky,skip_taskbar,skip_pager',  -- if own_window true - just hints - own_window_type sets it
    own_window_transparent = true,             -- if own_window_argb_visual is true sets background opacity 0%
    own_window_title = 'system_conky',          -- set the name manually  - default conky "hostname"
    own_window_type = 'override',                   -- if own_window true options are: normal/override/dock/desktop/panel
    own_window_transparent = true,
    on_window_argb_visual = true,


    --Colours

    default_color = '#ff0000',                  -- default color and border color
    color1 = '#FFFFFF',
    color2 = '#7aa2e2',
    color3 = '#cccccc',
    color4 = '#BDBDBD',
    color5 = '#CCCCCC',
    color6 = '#aa0000',

    --Signal Colours
    color7 = '#1F7411',                         --green
    color8 = '#FFA726',                         --orange
    color9 = '#F1544B',                         --firebrick


    --Lua
}
script = [[
  ${color #{color}}
  ${goto 60}${voffset 25}${font adele:size=25} ${time %A, %d %B}
  \
  # --- Separator line --- #
  ${goto 90}${voffset -}${font LG Weather_Z:size=100}${time %H:%M}${image /home/jicg/Personal/eleg-weather-conky/icons/#{theme}/line.png -p 360,30 -s 3x189}
  \
  ${offset 370}${voffset -183}${font ADELE:size=22}
  \
  # --- Weather --- #
  ###################
  \
  # --- WOEID (Location id) --- #
  ${execi 300 /home/jicg/Personal/eleg-weather-conky/scripts/weather.sh}\
  \
  # --- Temperature --- #
  #######################
  \
  ${font ADELE :size=30}${offset 260}${voffset 10}${execi 300 /home/jicg/Personal/eleg-weather-conky/scripts/kelvin2celsius.sh $(cat ~/.cache/eleg-weather.json | jq '.main.temp')}°${font ADELE :size=15}C${font ADELE :size=30}${voffset -20}  |
  \
  # --- Weather icon --- #
  ########################
  \
  ${execi 300 /home/jicg/Personal/eleg-weather-conky/scripts/weather-icon.sh #{theme} $(cat ~/.cache/eleg-weather.json | jq -r '.weather[0].icon')}${image ~/.cache/eleg-weather-icon.png -p 410,30 -s 100x100}
  \
  # --- Textual condition (e.g. Partly cloudy) --- #
  ##################################################
  \
  ${font Roboto Light:size=18}${offset 380}${voffset -82}${execi 300 cat ~/.cache/eleg-weather.json | jq -r '.weather[0].main'}
  \
  # --- Icon - high temperature --- #
  ###################################
  \
  ${image /home/jicg/Personal/eleg-weather-conky/icons/#{theme}/arrow-up.png -p 375,190 -s 12x12}
  \
  # --- High temperature --- #
  ############################
  \
  ${font Roboto Light:size=12}${offset 330}${voffset -25}${execi 300 /home/jicg/Personal/eleg-weather-conky/scripts/kelvin2celsius.sh $(cat ~/.cache/eleg-weather.json | jq '.main.temp_max')}°
  \
  # --- Icon - low temperature icon --- #
  #######################################
  \
  ${image /home/jicg/Personal/eleg-weather-conky/icons/#{theme}/arrow-down.png -p 422,190 -s 12x12}
  \
  # --- Low temperature --- #
  ###########################
  \
  ${font Roboto Light:size=12}${offset 400}${voffset -44}${execi 300 /home/jicg/Personal/eleg-weather-conky/scripts/kelvin2celsius.sh $(cat ~/.cache/eleg-weather.json | jq '.main.temp_min')}°
  \
  # --- Icon - map marker --- #
  #############################
  \
  ${image /home/jicg/Personal/eleg-weather-conky/icons/#{theme}/map-marker.png -p 463,187 -s 16x16}
  \
  # --- Location name (city) --- #
  ############################################
  \
  ${font Roboto Light:size=12}${offset 440}${voffset -45}${execi 300 cat ~/.cache/eleg-weather.json | jq -r '.name'}

  ${goto 285}${voffset -35}${font adele:bold:size=25}${time %p} \

  ${font Roboto Light:size=25}Humidity: ${execi 300 jq -r ".main.humidity" ~/.cache/eleg-weather.json}% \
  |   Wind: ${execi 300 jq -r ".wind.speed" ~/.cache/eleg-weather.json} m/s \
]];
local function interp (s, t)
  return s:gsub('(#%b{})', function (w)
      return t[w:sub(3, -2)] or w
  end)
end

function load(theme, color)
  return interp(script, {
    theme = theme,
    color = color
  })
end

conky.text = load('light', '#FFFFFF');
