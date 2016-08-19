"use strict";

function main_Init() {
    main_s = new main_S(10);
    main_s = new main_S(89);
    println(main_s);
}

function main_S(a) {
    this.x = a;
}
main_S.prototype.toString = (function() {
    return main_S_toString(this)
});

function main_S_toString(b) {
    return (((("S\{").toString() + ((b.x)).toString())).toString() + ("\}").toString());
}
var main_s;

function log(t) {
    console.log(t.toString())
}

function alert(t) {
    alert(t.toString())
}

function println(t) {
    stdout.innerHTML += t.toString() + "<br>"
}

function print(t) {
    stdout.innerHTML += t
}

function operator_add(t, r) {
    return t.operator_add(r)
}

function operator_sub(t, r) {
    return t.operator_sub(r)
}

function operator_mul(t, r) {
    return t.operator_mul(r)
}

function operator_div(t, r) {
    return t.operator_div(r)
}

function operator_pow(t, r) {
    return math.pow(t, r)
}

function unary_add(t) {
    return t
}

function unary_sub(t) {
    return -t
}

function newString(t) {
    return t.toString()
}

function string_toString(t) {
    return t
}

function int_toString(t) {
    return t.toString()
}

function float_toString(t) {
    return t.toString()
}

function array_toString(t) {
    return t.toString()
}

function log(t) {
    console.log(t.toString())
}

function List(t, r) {
    this.head = t, this.tail = r, null === r ? null === t ? this.length = 0 : this.length = 1 : this.length = r.length + 1
}

function listFromArray(t) {
    for (var r = t.length, n = EmptyList, e = 0; r > e; e++) n = n.append(t[e]);
    return n
}

function newList() {
    return listFromArray(Array.prototype.slice.call(arguments))
}

function newListRange(t, r) {
    for (var n = EmptyList, e = t; r > e; e++) n = n.append(e);
    return n
}

function newListInit(t, r) {
    for (var n = EmptyList, e = 0; t > e; e++) n = n.append(e);
    return n
}

function Vector(t, r, n) {
    this.shift = (n - 1) * this.bits, this.root = t, this.length = r, this.depth = n
}

function newVector() {
    return fromArray(Array.prototype.slice.call(arguments))
}

function fromArray(t) {
    for (var r = EmptyVector, n = 0; n < t.length; n++) r = r.append(t[n]);
    return r
}

function newVectorRange(t, r) {
    for (var n = EmptyVector, e = t; r > e; e++) n = n.append(e);
    return n
}

function newVectorInit(t, r) {
    for (var n = EmptyVector, e = 0; t > e; e++) n = n.append(e);
    return n
}
var stdout = document.getElementById("code");
Number.prototype.operator_add = function(t) {
    return this + t
}, Number.prototype.operator_div = function(t) {
    return this / t
}, Number.prototype.operator_sub = function(t) {
    return this - t
}, Number.prototype.operator_mul = function(t) {
    return this * t
}, Number.prototype.operator_equal = function(t) {
    return this == t
};
var EmptyList = new List(null, null);
List.prototype.append = function(t) {
    return new List(t, this)
}, List.prototype.toArray = function() {
    for (var t = [], r = this, n = 0; n < this.length; n++) t.push(r.head), r = r.tail;
    return t.reverse()
}, List.prototype.getProperIndex = function(t) {
    return 0 > t ? this.length + t : t
}, List.prototype.getList = function(t) {
    t = this.getProperIndex(t);
    for (var r = this.length - t - 1, n = this, e = 0; r > e; e++) n = n.tail;
    return n
}, List.prototype.get = function(t) {
    return this.getList(t).head
}, List.prototype.toString = function() {
    return "List(" + this.join(", ") + ")"
}, List.prototype.join = function(t) {
    null === t && (t = ",");
    var r = this;
    if (0 === this.length) return "";
    for (var n = r.head.toString(), e = 1; e < this.length; e++) r = r.tail, n = r.head.toString() + t.toString() + n;
    return n
}, List.prototype.insert = function(t, r) {
    function n(t, r, e) {
        if (0 > r) throw new Exception;
        return 0 === r ? t.append(e) : n(t.tail, r - 1, e).append(t.head)
    }
    return t = this.getProperIndex(t), n(this, this.length - t, r)
}, List.prototype.del = function(t) {
    function r(t, n) {
        if (0 > n) throw new Error("");
        if (1 === n) {
            var e = t.tail;
            return null === e && (e = EmptyList), e
        }
        return r(t.tail, n - 1).append(t.head)
    }
    return t = this.getProperIndex(t), r(this, this.length - t)
}, List.prototype.slice = function(t, r) {
    null == t && (t = 0), null == r && (r = this.length), r = this.getProperIndex(r - 1), t = this.getProperIndex(t);
    var n = this.getList(r),
        e = new List(n.head, n.tail);
    return e.length = r - t + 1, e
}, List.prototype.reverse = function() {
    for (var t = EmptyList, r = this, n = 0; n < this.length; n++) t = t.append(r.head), r = r.tail;
    return t
}, List.prototype.operator_equal = function(t) {
    if (this.length !== t.length) return !1;
    if (r === t) return !0;
    for (var r = this, n = 0; n < this.length; n++) {
        if (!r.head.operator_equal(t.head)) return !1;
        r = r.tail, t = t.tail
    }
    return !0
}, List.prototype.operator_add = function(t) {
    function r(t, n, e) {
        if (0 > n) throw new Exception;
        return 0 == n ? new List(e.head, e.tail) : r(t.tail, n - 1, e).append(t.head)
    }
    return r(t, t.length, this)
}, List.prototype.copy = function() {
    function t(r, n) {
        if (0 > n) throw new Exception;
        return 0 == n ? r : t(r.tail, n - 1).append(r.head)
    }
    return t(this, this.length)
}, List.prototype.set = function(t, r) {
    function n(t, r, e) {
        if (0 > r) throw new Exception;
        return 0 === r ? new List(e, t.tail) : n(t.tail, r - 1, e).append(t.head)
    }
    return t = this.getProperIndex(t), n(this, this.length - t - 1, r)
}, Vector.prototype.bits = 5, Vector.prototype.width = 1 << Vector.prototype.bits, Vector.prototype.mask = Vector.prototype.width - 1;
var EmptyVector = new Vector(Array(Vector.prototype.width), 0, 1);
Vector.prototype.get = function(t) {
    if (t >= this.length && 0 > t) throw new Error("out of bounds: " + t.toString());
    for (var r = this.root, n = this.bits, e = this.mask, o = this.shift; o > 0; o -= n) r = r[t >> o & e];
    return r[t & e]
}, Vector.prototype.append = function(t) {
    function r(i, s, h) {
        if (s > 0) {
            var u = h >> s & e;
            if (i) var p = i.slice();
            else var p = Array(o);
            return p[u] = r(p[u], s - n, h), p
        }
        var u = h & e;
        if (null == i) var p = Array(o);
        else var p = i.slice();
        return p[u] = t, p
    }
    var n = this.bits,
        e = this.mask,
        o = Vector.prototype.width;
    if (Math.pow(o, this.depth) === this.length) {
        var i = Array(o);
        i[0] = this.root, i[1] = Array(o);
        var s = r(i, this.depth * this.bits, this.length);
        return new Vector(s, this.length + 1, this.depth + 1)
    }
    var s = r(this.root, this.shift, this.length);
    return new Vector(s, this.length + 1, this.depth)
}, Vector.prototype.set = function(t, r) {
    function n(t, s, h) {
        if (s > 0) {
            var u = h >> s & o;
            if (t) var p = t.slice();
            else var p = Array(i);
            return p[u] = n(p[u], s - e, h), p
        }
        var u = h & o,
            p = t.slice();
        return p[u] = r, p
    }
    if (t >= this.length && 0 > t) throw new Error("out of bounds: " + t.toString());
    var e = this.bits,
        o = this.mask,
        i = Vector.prototype.width,
        s = n(this.root, this.shift, t);
    return new Vector(s, this.length, this.depth)
}, Vector.prototype.insert = function(t, r) {
    function n(t, r, h, u) {
        if (r > 0) {
            var p = h >> r & i;
            if (t) var a = t.slice();
            else var a = Array(s);
            var f = n(a[p], r - o, h, u);
            a[p] = f[0];
            var c = null;
            if (f[1]) {
                c = f[1];
                for (var l = p + 1; s > l; l++) {
                    var f = n(a[l], r - o, l << r, c);
                    a[l] = f[0], c = f[1]
                }
            }
            return [a, c]
        }
        var p = h & i;
        return e(t, p, u)
    }

    function e(t, r, n) {
        for (var e = [], o = 0; s - 1 > o; o++) r === o && e.push(n), e.push(t[o]);
        return r === o && e.push(n), [e, t[s - 1]]
    }
    if (t >= this.length && 0 > t) throw new Error("out of bounds: " + t.toString());
    var o = this.bits,
        i = this.mask,
        s = Vector.prototype.width,
        h = n(this.root, this.shift, t, r);
    return h[1] ? new Vector(h[0], this.length + 1, this.depth).append(h[1]) : new Vector(h[0], this.length + 1, this.depth)
}, Vector.prototype.toArray = function() {
    for (var t = Array(this.length), r = 0; r < this.length; r++) t[r] = this.get(r);
    return t
}, Vector.prototype.toString = function() {
    return "Vector(" + this.toArray().join(",") + ")"
}, Vector.prototype.operator_equal = function(t) {
    if (this.length !== t.length) return !1;
    if (this === t) return !0;
    for (var r = 0; r < this.length; r++)
        if (!this.get(r).operator_equal(t.get(r))) return !1;
    return !0
};