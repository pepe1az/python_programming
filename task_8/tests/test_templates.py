import unittest
from jinja2 import Environment, DictLoader, select_autoescape

class TestTemplates(unittest.TestCase):
    def test_render_loop(self):
        env = Environment(loader=DictLoader({
            "t.html": "{% for x in xs %}{{ x }} {% endfor %}"
        }), autoescape=select_autoescape())
        tpl = env.get_template("t.html")
        html = tpl.render(xs=[1, 2, 3])
        self.assertIn("1", html)
        self.assertIn("3", html)
