function bindOnchange(id, handler) {
    var selMaster = document.getElementById(id);
    if (selMaster.addEventListener) {
        // DOM2 standard
        selMaster.addEventListener("change", handler, false);
    }
    else if (box.attachEvent) {
        // IE fallback
        selMaster.attachEvent("onchange", handler);
    }
    else {
        // DOM0 fallback
        selMaster.onchange = handler;
    }
}
