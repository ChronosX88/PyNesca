#modules and selection and init args setup
config = {
    "parser" : 
    {
        "name":"Parser",
        "init_args":{}
    },
    "address_generator" :
    {
        "name":"IpGenerator",
        "init_args":{}
    },
    "scanner" : 
    { 
        "name":"FTPScanner",
        "init_args":{
            "credentials": (
                ("admin", "admin")
                )
            }
    },
    "storage" : 
    {
        "name":"JSONStorage",
        "init_args":
        {
            "path":"results.json",
            "json_scheme":
            {
                "ftp_status":
                [
                    {
                        "@ip":"ipv4_str",
                        "@port":"port",
                        "@login":"login",
                        "@password":"password",
                        "@ftp_version":"ftp_version",
                    }
                ]
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
'''scheme for gdocs scanner
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
'''
