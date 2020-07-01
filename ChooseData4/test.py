#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Charioty
# time:2020/3/12

a = 'U200009F01SS00N000001SQ001D0TY0Q48E40G1.75R2C7SL0BL0BR53GD1669@IGE$1@IPE$1@FG$100@FT$1@RC$0@IRC$0@PRC$0_p'

b = a[a.find('C'):a.find('SL')]

print(int(b[1:]))