loadjs.ready(["jquery", "mui"], {
    success: function() {
        "use strict";
        jQuery(function(e) {
            function t() {
                var t = {
                        onclose: function() {
                            i.removeClass("active").appendTo(document.body)
                        }
                    },
                    n = e(mui.overlay("on", t));
                i.appendTo(n), setTimeout(function() {
                    i.addClass("active")
                }, 20)
            }

            function n() {
                s.toggleClass("hide-sidedrawer")
            }

            function a() {
                c.scrollTop() > d ? u || (l.addClass("active"), u = !0) : u && (l.removeClass("active"), u = !1)
            }
            var s = e("body"),
                i = e("#sidedrawer"),
                r = e("#sidenav");
            ! function() {
                var t = e("strong", r);
                t.filter(":not(.active)").next().hide(), t.on("click", function() {
                    e(this).next().slideToggle(200)
                })
            }(), e("#appbar-sidenav-show").on("click", t), e("#appbar-sidenav-hide").on("click", n);
            var l = e("#header"),
                o = e("#f-hero"),
                c = e(window);
            if (o.length) {
                var d = o.height(),
                    u = !1;
                c.on("scroll", a), a()
            } else c.scrollTop() > 0 ? l.addClass("header-shadow") : c.one("scroll", function() {
                l.addClass("header-shadow")
            });
            setTimeout(function() {
                function t() {
                    var t = e('<div id="newsletter-banner" class="mui--text-subhead mui--z2"><div id="newsletter-banner-inner">Sign up for product alerts (monthly)<form><div class="mui-textfield"><input type="email" name="email" placeholder="Email address" spellcheck="false"></div><button class="mui-btn mui-btn--primary">Subscribe</button></form></div><div id="newsletter-banner-close">&times;</div>');
                    t.appendTo("body"), e("#newsletter-banner-close").on("click", function() {
                        t.remove(), n.setItem("newsletter-banner-close-ts", new Date), ga("send", "event", "newsletter-banner", "close", r)
                    }), e("form", t).on("submit", function(t) {
                        t.preventDefault();
                        var a = e(this),
                            s = e('input[name="email"]', a).val();
                        if (s.length) {
                            r = !0;
                            var i = e('<div id="newsletter-banner-social"/>');
                            i.append('<a href="https://github.com/muicss/mui" target="_blank"><i class="icon-github"></i></a>'), i.append('<a href="https://twitter.com/mui_css" target="_blank"><i class="icon-twitter"></i></a>'), e.post("/newsletter", a.serialize()).done(function() {
                                var t = "Thanks! You can follow us on Github and Twitter too!";
                                e("#newsletter-banner-inner").text(t).append(i), n.setItem("newsletter-status", "success")
                            }).fail(function() {
                                var t = "Sorry, there was a problem processing your request. Please try again later.";
                                e("#newsletter-banner-inner").text(t).append(i), n.setItem("newsletter-status", "fail")
                            }).always(function() {
                                n.setItem("newsletter-banner-close-ts", new Date)
                            }), ga("send", "event", "newsletter-banner", "submit", s)
                        }
                    }), ga("send", "event", "newsletter-banner", "render")
                }
                var n;
                try {
                    if (n = localStorage || null) {
                        var a, s = "_localStorageCheck",
                            i = new Date;
                        n.setItem(s, i), a = n.getItem(s) == i, n.removeItem(s), a || (n = null)
                    }
                } catch (e) {
                    n = null
                }
                if (null !== n && null === n.getItem("newsletter-banner-close-ts")) {
                    var r = !1;
                    t()
                }
            }, 3e4)
        })
    }
});

