#modules and selection and init args setup
config = {
    "parser" : 
    {
        "name":"GDocsHashParser",
        "init_args":{}
    },
    "address_generator" :
    {
        "name":"GDocsAddressGenerator",
        "init_args":{}
    },
    "scanner" : 
    { 
        "name":"GDocsScanner",
        "init_args":{}
    },
    "storage" : 
    {
        "name":"JSONStorage",
        "init_args":
        {
            "path":"results.json",
            "json_scheme":{
                "status":
                {
                    "gdoc_prefix":
                    [
                        {
                            "@hash": "gdoc_hash",
                            "@title": "gdoc_title"
                        }
                    ]
                }
            }
        }
    }
}

'''scheme for url scanner
{
    "status":
    {
        "url"
    }
}'''
'''scheme for port scanner
{
    "ipv4_str":
    {
        "port_status_str":
        {
            "port"
        }
    }
}'''
