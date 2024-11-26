import fh_fablib as fl


fl.require("1.0.20241122.2")
fl.config.update(
    app="mmmoney",
    host="www-data@feinheit06.nine.ch",
    domain="mmmoney.406.ch",
    branch="main",
    remote="production",
)

ns = fl.Collection(*fl.GENERAL, *fl.NINE)
