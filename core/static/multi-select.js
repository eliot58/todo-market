function MultiSelectTag(e, t = { shadow: !1, rounded: !0 }) {
    var n = null,
        l = null,
        d = null,
        a = null,
        s = null,
        i = null,
        o = null,
        r = null,
        c = null,
        u = null,
        p = null,
        v = null,
        m = t.tagColor || {},
        h = new DOMParser();
    function f(e = null) {
        for (var t of ((v.innerHTML = ""), l))
            if (t.selected) !w(t.value) && g(t);
            else {
                const n = document.createElement("li");
                (n.innerHTML = t.label), (n.dataset.value = t.value), e && t.label.toLowerCase().startsWith(e.toLowerCase()) ? v.appendChild(n) : e || v.appendChild(n);
            }
        const button = document.createElement("button");
        button.textContent = "Свой вариант"
        button.classList.add("button-1", "dark")
        button.style.padding = "12px 0px"
        button.style.borderRadius = "8px"
        button.style.fontWeight = "600"
        button.style.marginTop = "10px"
        button.style.width = "100%"
        button.type = "button"

        button.addEventListener("click", function(){
            
            const inp = document.createElement("input");
            inp.classList.add("input-field", "dark")
            inp.placeholder = "Введите свой вариант"
            inp.style.padding = "5px"
            inp.style.border = `1px solid #${localStorage.getItem('theme') == 'light' ? '2094AD' : '00A550'}`
            inp.addEventListener("keypress", function(event){
                if (event.keyCode == 13) {
                    const tags = document.querySelector("#tags")
                    const t = document.createElement("div");
                    t.classList.add("item-container");
                    const n = document.createElement("div");
                    n.classList.add("item-label"), (n.textContent = inp.value), (n.dataset.value = Number(v.querySelectorAll("li")[v.querySelectorAll("li").length -1].dataset.value) + 1);
                    const d = new DOMParser().parseFromString(
                        '<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="item-close-svg">\n                <line x1="18" y1="6" x2="6" y2="18"></line>\n                <line x1="6" y1="6" x2="18" y2="18"></line>\n                </svg>',
                        "image/svg+xml"
                    ).documentElement;
                    d.addEventListener("click", (t) => {
                        d.parentNode.remove()
                        for (const option of tags.querySelectorAll("option")) {
                            if (option.textContent == inp.value) {
                                option.remove()
                            }
                        }
                    }),
                        t.appendChild(n),
                        t.appendChild(d),
                        o.append(t);
                    tags.insertAdjacentHTML("beforeend", `<option selected value="${inp.value}">${inp.value}</option>`)
                    
                    inp.remove()
                }
            })
            v.insertBefore(inp, button)
        })
        v.appendChild(button)
    }
    function g(e) {
        const t = document.createElement("div");
        t.classList.add("item-container");
        const n = document.createElement("div");
        n.classList.add("item-label"), (n.innerHTML = e.label), (n.dataset.value = e.value);
        const d = new DOMParser().parseFromString(
            '<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="item-close-svg">\n                <line x1="18" y1="6" x2="6" y2="18"></line>\n                <line x1="6" y1="6" x2="18" y2="18"></line>\n                </svg>',
            "image/svg+xml"
        ).documentElement;
        d.addEventListener("click", (t) => {
            (l.find((t) => t.value == e.value).selected = !1), C(e.value), f(), E();
        }),
            t.appendChild(n),
            t.appendChild(d),
            o.append(t);
    }
    function L() {
        for (var e of v.querySelectorAll("li"))
            e.addEventListener("click", (e) => {
                (l.find((t) => t.value == e.target.dataset.value).selected = !0), (c.value = null), f(), E(), c.focus();
            });
    }
    function w(e) {
        for (var t of o.children) if (!t.classList.contains("input-body") && t.firstChild.dataset.value == e) return !0;
        return !1;
    }
    function C(e) {
        for (var t of o.children) t.classList.contains("input-body") || t.firstChild.dataset.value != e || o.removeChild(t);
    }
    function E(e = !0) {
        selected_values = [];
        for (var d = 0; d < l.length; d++) (n.options[d].selected = l[d].selected), l[d].selected && selected_values.push({ label: l[d].label, value: l[d].value });
        e && t.hasOwnProperty("onChange") && t.onChange(selected_values);
    }
    (n = document.getElementById(e)),
        (function () {
            (l = [...n.options].map((e) => ({ value: e.value, label: e.label, selected: e.selected }))),
                n.classList.add("hidden"),
                (d = document.createElement("div")).classList.add("mult-select-tag"),
                d.classList.add(localStorage.getItem('theme') == 'light' ? 'light' : 'dark'),
                (a = document.createElement("div")).classList.add("wrapper"),
                (i = document.createElement("div")).classList.add("body"),
                t.shadow && i.classList.add("shadow"),
                t.rounded && i.classList.add("rounded"),
                (o = document.createElement("div")).classList.add("input-container"),
                (o.textContent = "Тэги"),
                (c = document.createElement("input")).classList.add("input"),
                (c.placeholder = `${t.placeholder || "Поиск..."}`),
                (r = document.createElement("inputBody")).classList.add("input-body"),
                r.append(c),
                i.append(o),
                (s = document.createElement("div")).classList.add("btn-container"),
                ((u = document.createElement("button")).type = "button"),
                s.append(u);
            const e = h.parseFromString(
                '<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">\n            <polyline points="18 15 12 21 6 15"></polyline></svg>',
                "image/svg+xml"
            ).documentElement;
            u.append(e),
                i.append(s),
                a.append(i),
                (p = document.createElement("div")).classList.add("drawer", "hidden"),
                t.shadow && p.classList.add("shadow"),
                t.rounded && p.classList.add("rounded"),
                p.append(r),
                (v = document.createElement("ul")),
                p.appendChild(v),
                d.appendChild(a),
                d.appendChild(p),
                n.nextSibling ? n.parentNode.insertBefore(d, n.nextSibling) : n.parentNode.appendChild(d);
        })(),
        f(),
        L(),
        E(!1),
        u.addEventListener("click", () => {
            (f(), L(), p.classList.toggle("hidden", p.classList.toggle("hidden")), c.focus());
        }),
        c.addEventListener("keyup", (e) => {
            f(e.target.value), L();
        }),
        c.addEventListener("keydown", (e) => {
            if ("Backspace" === e.key && !e.target.value && o.childElementCount > 1) {
                const e = i.children[o.childElementCount - 2].firstChild;
                (l.find((t) => t.value == e.dataset.value).selected = !1), C(e.dataset.value), E();
            }
        }),
        window.addEventListener("click", (e) => {
            d.contains(e.target) || p.classList.add("hidden");
        });
}
