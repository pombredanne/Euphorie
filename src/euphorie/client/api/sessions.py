from five import grok
from z3c.saconfig import Session
from euphorie.content.survey import ISurvey
from euphorie.client.survey import PathGhost
from euphorie.client.model import SurveySession
from euphorie.client.api import JsonView
from euphorie.client.api.session import View as SessionView
from euphorie.client.api.session import get_survey
from euphorie.client.profile import set_session_profile
from euphorie.client.session import create_survey_session



class Sessions(PathGhost):
    """Virtual container for all user data."""

    def __init__(self, id, request, account):
        super(Sessions, self).__init__(id, request)
        self.account = account

    def __getitem__(self, key):
        try:
            survey_session = Session.query(SurveySession)\
                    .filter(SurveySession.id == int(key))\
                    .filter(SurveySession.account == self.account)\
                    .first()
            survey = get_survey(self.request, survey_session.zodb_path)
            if survey is not None:
                self.request.survey = survey
                return survey_session.__of__(self)
        except (AttributeError, TypeError, ValueError):
            pass

        raise KeyError(key)


class View(JsonView):
    grok.context(Sessions)
    grok.require('zope2.View')
    grok.name('index_html')

    def sessions(self):
        return [{'id': session.id,
                 'title': session.title,
                 'created': session.modified.isoformat(),
                 'modified': session.modified.isoformat()}
                for session in self.context.account.sessions]

    def GET(self):
        return {'sessions': self.sessions()}

    def POST(self):
        try:
            survey = self.request.client.restrictedTraverse(
                    self.input['survey'].split('/'))
            if not ISurvey.providedBy(survey):
                raise TypeError('Not a survey')
        except (KeyError, TypeError):
            return {'type': 'error',
                    'message': 'Unknown survey'}

        title = self.input.get('title', survey.title)
        survey_session = create_survey_session(title, survey)
        view = SessionView(survey_session, self.request)
        response = view.GET()
        survey_session_url = self.context.absolute_url()
        if survey.ProfileQuestions():
            response['next-step'] = '%s/profile' % survey_session_url
        else:
            survey_session = set_session_profile(survey, survey_session, {})
            response['next-step'] = '%s/identification' % survey_session_url
        return response
