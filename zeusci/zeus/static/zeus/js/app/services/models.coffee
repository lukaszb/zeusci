
# TODO: Generalize URLs below (so they are not hardcoded here)
zeus.API_PROJECT_DETAIL_URL = '/api/projects/:name.json'
zeus.API_BUILDSET_DETAIL_URL = '/api/projects/:name/buildsets/:buildsetNo.json'
zeus.API_BUILD_DETAIL_URL = '/api/projects/:name/builds/:buildsetNo.:buildNo.json'


zeus.factory 'Project', ($resource) ->
    Project = $resource(zeus.API_PROJECT_DETAIL_URL, {}, {
        query: {method: 'GET'},
    })
    Project.getInstance = () ->
        return zeus_project
    return Project


zeus.factory 'Buildset', ($resource) ->
    Buildset = $resource(zeus.API_BUILDSET_DETAIL_URL, {}, {
        query: {method: 'GET'},
    })
    return Buildset


zeus.factory 'Build', ($resource) ->
    Build = $resource(zeus.API_BUILD_DETAIL_URL, {}, {
        query: {method: 'GET'},
    })
    return Build

