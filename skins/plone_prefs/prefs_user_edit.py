## Script (Python) "prefs_user_edit"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=userid, portrait='',delete_portrait=''
##title=Edit user
##
#update portrait
REQUEST=context.REQUEST
portal_membership = context.portal_membership
member=portal_membership.getMemberById(userid)
if portrait:
    portrait.seek(0)
    portal_membership.changeMemberPortrait(portrait, userid)

if delete_portrait:
    context.portal_membership.deletePersonalPortrait(member.getId())

processed={}
for id, property in context.portal_memberdata.propertyItems():
    if id == 'last_login_time':
        continue
    processed[id]=REQUEST.get(id, None)

context.plone_utils.setMemberProperties(member, **processed)


REFERER=REQUEST.HTTP_REFERER
if REFERER.find('portal_status_message')!=-1:
    REFERER=REFERER[:REFERER.find('portal_status_message')]
url='%s&%s' % (REFERER, 'portal_status_message=Changes+made.')
return REQUEST.RESPONSE.redirect(url)
