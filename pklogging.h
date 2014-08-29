/******************************************************************************
utils.h - Logging.

This file is Copyright 2011-2014, The Beanstalks Project ehf.

This program is free software: you can redistribute it and/or modify it under
the terms  of the  Apache  License 2.0  as published by the  Apache  Software
Foundation.

This program is distributed in the hope that it will be useful,  but  WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the Apache License for more details.

You should have received a copy of the Apache License along with this program.
If not, see: <http://www.apache.org/licenses/>

Note: For alternate license terms, see the file COPYING.md.

******************************************************************************/

#define PK_LOG_TUNNEL_DATA     0x0001
#define PK_LOG_TUNNEL_HEADERS  0x0002
#define PK_LOG_TUNNEL_CONNS    0x0004
#define PK_LOG_BE_DATA         0x0010
#define PK_LOG_BE_HEADERS      0x0020
#define PK_LOG_BE_CONNS        0x0040
#define PK_LOG_MANAGER_ERROR   0x0100
#define PK_LOG_MANAGER_INFO    0x0200
#define PK_LOG_MANAGER_DEBUG   0x0400

#define PK_LOG_TRACE           0x0800
#define PK_LOG_ERROR           0x1000

#define PK_LOG_ERRORS          (PK_LOG_ERROR|PK_LOG_MANAGER_ERROR)
#define PK_LOG_MANAGER         (PK_LOG_MANAGER_ERROR|PK_LOG_MANAGER_INFO)
#define PK_LOG_CONNS           (PK_LOG_BE_CONNS|PK_LOG_TUNNEL_CONNS)
#define PK_LOG_NORMAL          (PK_LOG_ERRORS|PK_LOG_CONNS|PK_LOG_MANAGER)
#define PK_LOG_DEBUG           (PK_LOG_NORMAL|PK_LOG_MANAGER_DEBUG)
#define PK_LOG_ALL             0xffff

#if defined(PK_TRACE) && (PK_TRACE >= 1)
#define PK_TRACE_FUNCTION pk_log(PK_LOG_TRACE, "trace/%s", __FUNCTION__)
#define PK_TRACE_LOOP(msg) pk_log(PK_LOG_TRACE, "trace/%s: %s", __FUNCTION__, msg)
#else
#define PK_TRACE_FUNCTION
#define PK_TRACE_LOOP(msg)
#endif

int pk_log(int, const char *fmt, ...);
int pk_log_chunk(struct pk_chunk*);
void pk_dump_parser(char*, struct pk_parser*);
void pk_dump_conn(char*, struct pk_conn*);
void pk_dump_tunnel(char*, struct pk_tunnel*);
void pk_dump_be_conn(char*, struct pk_backend_conn*);
void pk_dump_state(struct pk_manager*);

