#!/usr/bin/env python3
# Write ch00 Chinese SVG using XML numeric character references (pure ASCII)

content = r"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 560" width="860" height="560">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">
      <path d="M 0 1 L 9 5 L 0 9 z" fill="#5b9bd5"/>
    </marker>
  </defs>

  <rect width="860" height="560" fill="#ffffff" rx="6"/>

  <rect x="30" y="15" width="800" height="40" fill="#1a3a5c" rx="6"/>
  <text x="430" y="42" font-family="Arial, sans-serif" font-size="15" fill="#ffffff" text-anchor="middle" font-weight="bold">2500&#24180;&#20859;&#29983;&#26234;&#24935; &#183; &#20840;&#20070;&#26550;&#26500;</text>

  <rect x="300" y="75" width="260" height="55" fill="#2d5a88" rx="6"/>
  <text x="430" y="98" font-family="Arial, sans-serif" font-size="13" fill="#ffffff" text-anchor="middle" font-weight="bold">&#31532;&#19968;&#31456; &#26368;&#21476;&#32769;&#30340;&#23545;&#35805;</text>
  <text x="430" y="116" font-family="Arial, sans-serif" font-size="11" fill="#f0f0f0" text-anchor="middle">&#36208;&#36827;&#20869;&#32463;&#65292;&#25645;&#24314;&#33310;&#21488;</text>

  <path d="M 430 130 L 132 168" stroke="#5b9bd5" stroke-width="2" fill="none" marker-end="url(#arrow)"/>
  <path d="M 430 130 L 332 168" stroke="#5b9bd5" stroke-width="2" fill="none" marker-end="url(#arrow)"/>
  <path d="M 430 130 L 532 168" stroke="#5b9bd5" stroke-width="2" fill="none" marker-end="url(#arrow)"/>
  <path d="M 430 130 L 732 168" stroke="#5b9bd5" stroke-width="2" fill="none" marker-end="url(#arrow)"/>

  <rect x="38" y="170" width="188" height="70" fill="#5b9bd5" rx="6"/>
  <text x="132" y="195" font-family="Arial, sans-serif" font-size="13" fill="#ffffff" text-anchor="middle" font-weight="bold">&#31532;&#20108;&#31456; &#39034;&#26102;&#32780;&#27963;</text>
  <text x="132" y="214" font-family="Arial, sans-serif" font-size="11" fill="#f0f0f0" text-anchor="middle">&#26172;&#22812;&#33410;&#24459;</text>

  <rect x="238" y="170" width="188" height="70" fill="#5b9bd5" rx="6"/>
  <text x="332" y="195" font-family="Arial, sans-serif" font-size="13" fill="#ffffff" text-anchor="middle" font-weight="bold">&#31532;&#19977;&#31456; &#39135;&#20859;&#20043;&#36947;</text>
  <text x="332" y="214" font-family="Arial, sans-serif" font-size="11" fill="#f0f0f0" text-anchor="middle">&#20116;&#21619;&#35843;&#21644;</text>

  <rect x="438" y="170" width="188" height="70" fill="#5b9bd5" rx="6"/>
  <text x="532" y="195" font-family="Arial, sans-serif" font-size="13" fill="#ffffff" text-anchor="middle" font-weight="bold">&#31532;&#22235;&#31456; &#24773;&#24535;&#20043;&#20307;</text>
  <text x="532" y="214" font-family="Arial, sans-serif" font-size="11" fill="#f0f0f0" text-anchor="middle">&#24515;&#36523;&#20813;&#30123;</text>

  <rect x="638" y="170" width="188" height="70" fill="#5b9bd5" rx="6"/>
  <text x="732" y="195" font-family="Arial, sans-serif" font-size="13" fill="#ffffff" text-anchor="middle" font-weight="bold">&#31532;&#20116;&#31456; &#24418;&#21160;&#22914;&#27700;</text>
  <text x="732" y="214" font-family="Arial, sans-serif" font-size="11" fill="#f0f0f0" text-anchor="middle">&#26580;&#24615;&#36816;&#21160;</text>

  <path d="M 132 240 L 430 288" stroke="#5b9bd5" stroke-width="2" fill="none" marker-end="url(#arrow)"/>
  <path d="M 332 240 L 430 288" stroke="#5b9bd5" stroke-width="2" fill="none" marker-end="url(#arrow)"/>
  <path d="M 532 240 L 430 288" stroke="#5b9bd5" stroke-width="2" fill="none" marker-end="url(#arrow)"/>
  <path d="M 732 240 L 430 288" stroke="#5b9bd5" stroke-width="2" fill="none" marker-end="url(#arrow)"/>

  <rect x="38" y="290" width="784" height="50" fill="#2d5a88" rx="6"/>
  <text x="430" y="312" font-family="Arial, sans-serif" font-size="13" fill="#ffffff" text-anchor="middle" font-weight="bold">&#31532;&#20845;&#31456; &#27835;&#26410;&#30149;&#30340;&#33402;&#26415;</text>
  <text x="430" y="330" font-family="Arial, sans-serif" font-size="11" fill="#f0f0f0" text-anchor="middle">&#39044;&#38450;&#21307;&#23398;&#24635;&#26694;&#26550;</text>

  <path d="M 430 340 L 275 383" stroke="#5b9bd5" stroke-width="2" fill="none" marker-end="url(#arrow)"/>
  <path d="M 430 340 L 585 383" stroke="#5b9bd5" stroke-width="2" fill="none" marker-end="url(#arrow)"/>

  <rect x="150" y="385" width="250" height="55" fill="#5b9bd5" rx="6"/>
  <text x="275" y="408" font-family="Arial, sans-serif" font-size="13" fill="#ffffff" text-anchor="middle" font-weight="bold">&#31532;&#19971;&#31456; &#24179;&#34913;&#65292;&#32780;&#38750;&#23436;&#32654;</text>
  <text x="275" y="426" font-family="Arial, sans-serif" font-size="11" fill="#f0f0f0" text-anchor="middle">&#38452;&#38451;&#24179;&#34913;</text>

  <rect x="460" y="385" width="250" height="55" fill="#5b9bd5" rx="6"/>
  <text x="585" y="408" font-family="Arial, sans-serif" font-size="13" fill="#ffffff" text-anchor="middle" font-weight="bold">&#31532;&#20843;&#31456; &#30561;&#30496;&#65306;&#26368;&#22909;&#30340;&#20462;&#22797;</text>
  <text x="585" y="426" font-family="Arial, sans-serif" font-size="11" fill="#f0f0f0" text-anchor="middle">&#20462;&#22797;&#31995;&#32479;</text>

  <path d="M 275 440 L 430 488" stroke="#5b9bd5" stroke-width="2" fill="none" marker-end="url(#arrow)"/>
  <path d="M 585 440 L 430 488" stroke="#5b9bd5" stroke-width="2" fill="none" marker-end="url(#arrow)"/>

  <rect x="38" y="490" width="784" height="50" fill="#1a3a5c" rx="6"/>
  <text x="430" y="512" font-family="Arial, sans-serif" font-size="13" fill="#ffffff" text-anchor="middle" font-weight="bold">&#31532;&#20061;&#31456; 90&#22825;&#20859;&#29983;&#37325;&#21551;</text>
  <text x="430" y="530" font-family="Arial, sans-serif" font-size="11" fill="#f0f0f0" text-anchor="middle">&#20840;&#38754;&#25972;&#21512;&#19982;&#34892;&#21160;&#35745;&#21010;</text>
</svg>"""

import os
target = r'c:\Users\wan_f\Desktop\cursor\AI工作台\output\book-yellow-emperor\images\ch00-fig1-book-architecture.svg'
with open(target, 'w', encoding='ascii', newline='\n') as f:
    f.write(content)
print('Written:', os.path.getsize(target), 'bytes')

# Verify
with open(target, 'r', encoding='ascii') as f:
    text = f.read()
    assert '&#31532;' in text
    assert '&#20859;' in text
print('Verification passed - XML entities preserved correctly')
