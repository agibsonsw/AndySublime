import sublime, sublime_plugin
import re

def match(rex, str):
    m = rex.match(str)
    if m:
        return m.group(0)
    else:
        return None

# This responds to on_query_completions, but conceptually it's expanding
# expressions, rather than completing words.
#
# It expands these simple expressions:
# tag.class
# tag#id
class HtmlCompletions(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        # Only trigger within HTML
        if not view.match_selector(locations[0],
                "text.html - source - meta.tag, punctuation.definition.tag.begin"):
            return []

        # Get the contents of each line, from the beginning of the line to
        # each point
        lines = [view.substr(sublime.Region(view.line(l).a, l))
            for l in locations]

        # Reverse the contents of each line, to simulate having the regex
        # match backwards
        lines = [l[::-1] for l in lines]

        # Check the first location looks like an expression
        rex = re.compile("([\w-]+)([.#])(\w+)")
        expr = match(rex, lines[0])
        if not expr:
            return []

        # Ensure that all other lines have identical expressions
        for i in xrange(1, len(lines)):
            ex = match(rex, lines[i])
            if ex != expr:
                return []

        # Return the completions
        arg, op, tag = rex.match(expr).groups()

        arg = arg[::-1]
        tag = tag[::-1]
        expr = expr[::-1]

        if op == '.':
            snippet = "<{0} class=\"{1}\">$1</{0}>$0".format(tag, arg)
        else:
            snippet = "<{0} id=\"{1}\">$1</{0}>$0".format(tag, arg)

        return [(expr, snippet)]


# Provide completions that match just after typing an opening angle bracket
class TagCompletions(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        # Only trigger within HTML
        if not view.match_selector(locations[0],
                "text.html -source -meta.tag, punctuation.definition.tag.begin"):
            return []

        pt = locations[0] - len(prefix) - 1
        ch = view.substr(sublime.Region(pt, pt + 1))
        if ch != '<':
            return []

        return ([
            ("a\tTag", "a href=\"$1\">$2</a>"),
            ("abbr\tTag", "abbr>$1</abbr>"),
            ("acronym\tRemoved", "acronym>$1</acronym>"),
            ("address\tTag", "address>$1</address>"),
            ("applet\tRemoved", "applet>$1</applet>"),
            ("area\tTag", "area>$1</area>"),
            ("article\tHTML5", "article>$1</article>"),
            ("aside\tHTML5", "aside>$1</aside>"),
            ("audio\tHTML5", "audio>$1</audio>"),
            ("b\tTag", "b>$1</b>"),
            ("base\tTag", "base href=\"$1\">"),
            ("big\tRemoved", "big>$1</big>"),
            ("blockquote\tTag", "blockquote>$1</blockquote>"),
            ("body\tTag", "body>$1</body>"),
            ("br\tTag", "br>"),
            ("button\tTag", "button>$1</button>"),
            ("canvas\tHTML5", "canvas width=\"$1\" height=\"$2\">${3:Browser does not support 'canvas' tag.}</canvas>"),
            ("caption\tTag", "caption>$1</caption>"),
            ("cdata\tTag", "cdata>$1</cdata>"),
            ("center\tRemoved", "center>$1</center>"),
            ("cite\tTag", "cite>$1</cite>"),
            ("code\tTag", "code>$1</code>"),
            ("col\tTag", "col>$1</col>"),
            ("colgroup\tTag", "colgroup>$1</colgroup>"),
            ("command\tHTML5", "command>$1</command>"),
            ("datalist\tHTML5", "datalist>$1</datalist>"),
            ("dd\tTag", "dd>$1</dd>"),
            ("del\tTag", "del>$1</del>"),
            ("details\tHTML5", "details>$1</details>"),
            ("dfn\tTag", "dfn>$1</dfn>"),
            ("div\tTag", "div>$1</div>"),
            ("dl\tTag", "dl>$1</dl>"),
            ("dt\tTag", "dt>$1</dt>"),
            ("em\tTag", "em>$1</em>"),
            ("embed\tTag", "embed>"),
            ("fieldset\tTag", "fieldset>$1</fieldset>"),
            ("figure\tHTML5", "figure>$1</figure>"),
            ("font\tRemoved", "font>$1</font>"),
            ("footer\tHTML5", "footer>$1</footer>"),
            ("form\tTag", "form action=\"$1\" method=\"${2:Get/Post}${2/(g$)|(p$)|.*/?1:et:?2:ost/i}\">$3</form>"),
            ("frame\tRemoved", "frame>$1</frame>"),
            ("frameset\tRemoved", "frameset>$1</frameset>"),
            ("h1\tTag", "h1>$1</h1>"),
            ("h2\tTag", "h2>$1</h2>"),
            ("h3\tTag", "h3>$1</h3>"),
            ("h4\tTag", "h4>$1</h4>"),
            ("h5\tTag", "h5>$1</h5>"),
            ("h6\tTag", "h6>$1</h6>"),
            ("head\tTag", "head>$1</head>"),
            ("header\tHTML5", "header>$1</header>"),
            ("hgroup\tHTML5", "hgroup>$1</hgroup>"),
            ("hr\tTag", "hr>"),
            ("html\tTag", "html>$1</html>"),
            ("i\tTag", "i>$1</i>"),
            ("iframe\tTag", "iframe src=\"$1\"></iframe>"),
            ("img\tTag", "img src=\"$1\">"),
            ("input\tTag", "input type=\"$1${1/(b$)|(co$)|(c$)|(dat$)|(da$)|(d$)|(e$)|(f$)|(h$)|(i$)|(m$)|(n$)|(p$)|(ra$)|(r$)|(su$)|(se$)|(s$)|(te$)|(ti$)|(t$)|(u$)|(w$)|.*/?1:utton:?2:lor:?3:heckbox:?4:etime-local:?5:tetime:?6:ate:?7:mail:?8:ile:?9:idden:?10:mage:?11:onth:?12:umber:?13:assword:?14:nge:?15:adio:?16:bmit:?17:arch:?18:elect:?19:xtarea:?20:me:?21:ext:?22:rl:?23:eek/i}\">"),
            ("ins\tTag", "ins>$1</ins>"),
            ("kbd\tTag", "kbd>$1</kbd>"),
            ("keygen\tHTML5", "keygen>$1</keygen>"),
            ("label\tTag", "label>$1</label>"),
            ("legend\tTag", "legend>$1</legend>"),
            ("li\tTag", "li>$1</li>"),
            ("link\tTag", "link rel=\"stylesheet\" type=\"text/css\" href=\"$1\">"),
            ("map\tTag", "map>$1</map>"),
            ("mark\tHTML5", "mark>$1</mark>"),
            ("meta\tTag", "meta>"),
            ("meter\tHTML5", "meter>$1</meter>"),
            ("nav\tHTML5", "nav>$1</nav>"),
            ("noframes\tRemoved", "noframes>$1</noframes>"),
            ("object\tTag", "object>$1</object>"),
            ("ol\tTag", "ol>$1</ol>"),
            ("optgroup\tTag", "optgroup>$1</optgroup>"),
            ("option\tTag", "option>$1</option>"),
            ("output\tHTML5", "output>$1</output>"),
            ("p\tTag", "p>$1</p>"),
            ("param\tTag", "param name=\"$1\" value=\"$2\">"),
            ("pre\tTag", "pre>$1</pre>"),
            ("progress\tHTML5", "progress>$1</progress>"),
            ("ruby\tHTML5", "ruby>$1</ruby>"),
            ("samp\tTag", "samp>$1</samp>"),
            ("script\tTag", "script type=\"${1:text/javascript}\">$2</script>"),
            ("section\tHTML5", "section>$1</section>"),
            ("select\tTag", "select>$1</select>"),
            ("small\tTag", "small>$1</small>"),
            ("span\tTag", "span>$1</span>"),
            ("strong\tTag", "strong>$1</strong>"),
            ("style\tTag", "style type=\"${1:text/css}\">$2</style>"),
            ("sub\tTag", "sub>$1</sub>"),
            ("summary\tHTML5", "summary>$1</summary>"),
            ("sup\tTag", "sup>$1</sup>"),
            ("table\tTag", "table>$1</table>"),
            ("tbody\tTag", "tbody>$1</tbody>"),
            ("td\tTag", "td>$1</td>"),
            ("textarea\tTag", "textarea>$1</textarea>"),
            ("tfoot\tTag", "tfoot>$1</tfoot>"),
            ("th\tTag", "th>$1</th>"),
            ("thead\tTag", "thead>$1</thead>"),
            ("time\tHTML5", "time>$1</time>"),
            ("title\tTag", "title>$1</title>"),
            ("tr\tTag", "tr>$1</tr>"),
            ("tt\tRemoved", "tt>$1</tt>"),
            ("u\tRemoved", "u>$1</u>"),
            ("ul\tTag", "ul>$1</ul>"),
            ("var\tTag", "var>$1</var>"),
            ("video\tTag", "video>$1</video>"),
            ("wbr\tHTML5", "wbr>$1</wbr>")
        ], sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS)
