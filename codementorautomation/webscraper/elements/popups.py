from selenium_objects import Element, Selector


class InstantHelpRequestPopup(Element):
    selector = Selector(by='css selector', value='.instant-help-enter-done')


class SessionNoticePopup(Element):
    selector = Selector(by='css selector', value='.session-notice')