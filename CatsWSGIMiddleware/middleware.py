try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

from webob import Request


class CatsMiddleware(object):
    """
        Kitten middleware
                  T."-._..---.._,-"/|
                  l|"-.  _.v._   (" |
                  [l /.'_ \; _~"-.`-t
                  Y " _(o} _{o)._ ^.|
                  j  T  ,-<v>-.  T  ]
                  \  l ( /-^-\ ) !  !
                   \. \.  "~"  ./  /c-..,__
                     ^r- .._ .- .-"  `- .  ~"--.
                      > \.                      \
                      ]   ^.                     \
                      3  .  ">            .       Y
         ,.__.--._   _j   \ ~   .         ;       |
        (    ~"-._~"^._\   ^.    ^._      I     . l
         "-._ ___ ~"-,_7    .Z-._   7"   Y      ;  \        _
            /"   "~-(r r  _/_--._~-/    /      /,.--^-._   / Y
            "-._    '"~~~>-._~]>--^---./____,.^~        ^.^  !
                ~--._    '   Y---.                        \./
                     ~~--._  l_   )                        \
                           ~-._~~~---._,____..---           \
                               ~----"~       \
                                              \
        
    """
    def __init__(self, app, i_hate_cats=False):
        """
        Middleware Constructor
        :param app: WSGI app
        :param i_hate_cats: think before construct a middleware instance
        """
        self.app = app
        self.active_all = i_hate_cats

    def __call__(self, environ, start_response):
        """
        Middleware itselfstau
        :param environ: 
        :param start_response: 
        :return: 
        """
        request = Request(environ)
        wants_a_cat = request.headers.get('Cats')
        response = request.get_response(self.app, catch_exc_info=True)
        if _i_need_a_cat(response.status_code, self.active_all, wants_a_cat):
            response.body = _get_a_cat(response.status_code)
            response.headers['Cats'] = '=^..^='
        return response(environ, start_response)


def _i_need_a_cat(status_code, active, want):
    """
    This function tell you if you need a cat in your response
    :param status_code: response status_code
    :param active: activated
    :param want: want it right now 
    :return: True if you needed, false otherwise
    """
    return status_code > 400 or active or want is not None


def _get_a_cat(status_code):
    """
    This download the binary data about some cats
    :param status_code: response status_code
    :return: a kitten
    """
    return urlopen('https://http.cat/{}'.format(status_code)).read()
