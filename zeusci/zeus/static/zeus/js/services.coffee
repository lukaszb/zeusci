
zeus.API_PROJECT_DETAIL_URL = '/api/projects/:name.json'
zeus.API_BUILDSET_DETAIL_URL = '/api/projects/:name/buildsets/:buildsetNo.json'
zeus.API_BUILD_DETAIL_URL = '/api/projects/:name/builds/:buildsetNo.:buildNo.json'

zeus.factory('Project', ($resource) ->
    return $resource(zeus.API_PROJECT_DETAIL_URL, {}, {
        query: {
            method: 'GET',
        },
    })
)

zeus.factory('Buildset', ($resource) ->
    return $resource(zeus.API_BUILDSET_DETAIL_URL, {}, {
        query: {
            method: 'GET',
            params: {name: zeus_project.name},
        },
    })
)

zeus.factory('Build', ($resource) ->
    return $resource(zeus.API_BUILD_DETAIL_URL, {}, {
        query: {
            method: 'GET',
            params: {name: zeus_project.name, buildsetNo: zeus_buildset.number},
        },
    })
)

