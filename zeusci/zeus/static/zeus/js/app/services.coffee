
# TODO: Generalize URLs below (so they are not hardcoded here)
zeus.API_PROJECT_DETAIL_URL = '/api/projects/:name.json'
zeus.API_BUILDSET_DETAIL_URL = '/api/projects/:name/buildsets/:buildsetNo.json'
zeus.API_BUILD_DETAIL_URL = '/api/projects/:name/builds/:buildsetNo.:buildNo.json'

window = @

zeus.factory 'Project', ($resource) ->
    Project = $resource(zeus.API_PROJECT_DETAIL_URL, {}, {
        query: {method: 'GET'},
    })
    Project.getInstance = () ->
        return zeus_project
    # XXX: helper, remove it (this won't work unless Project is injected somewhere)
    window.Project = Project
    return Project

