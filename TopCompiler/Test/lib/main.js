function main_Init(){main_s = new main_S(10);main_s = new main_S(89);println(main_s);}function main_S(a){this.x=a;}main_S.prototype.toString=(function(){return main_S_toString(this)});function main_S_toString(b){return (((("S\{").toString()+((b.x)).toString())).toString()+("\}").toString());}var main_s;