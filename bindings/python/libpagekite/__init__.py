###############################################################################
#    libpagekite-Python - Wrappers for the libpagekite API
# 
#       * * *   WARNING: This file is auto-generated, do not edit!  * * *
# 
###############################################################################
# This file is Copyright 2012-2016, The Beanstalks Project ehf.
# 
# This program is free software: you can redistribute it and/or modify it under
# the terms  of the  Apache  License 2.0  as published by the  Apache  Software
# Foundation.
# 
# This program is distributed in the hope that it will be useful,  but  WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the Apache License for more details.
# 
# You should have received a copy of the Apache License along with this program.
# If not, see: <http://www.apache.org/licenses/>
# 
# Note: For alternate license terms, see the file COPYING.md.
###############################################################################


PK_VERSION = "0.90.160219C"
PK_STATUS_STARTUP = 10
PK_STATUS_CONNECTING = 20
PK_STATUS_UPDATING_DNS = 30
PK_STATUS_FLYING = 40
PK_STATUS_PROBLEMS = 50
PK_STATUS_REJECTED = 60
PK_STATUS_NO_NETWORK = 90
PK_WITH_DEFAULTS = 0x0000
PK_WITHOUT_DEFAULTS = 0x1000
PK_WITH_SSL = 0x0001
PK_WITH_IPV4 = 0x0002
PK_WITH_IPV6 = 0x0004
PK_WITH_SERVICE_FRONTENDS = 0x0008
PK_WITHOUT_SERVICE_FRONTENDS = 0x0010
PK_WITH_DYNAMIC_FE_LIST = 0x0020
PK_AS_FRONTEND_RELAY = 0x0100
PK_LOG_TUNNEL_DATA = 0x000100
PK_LOG_TUNNEL_HEADERS = 0x000200
PK_LOG_TUNNEL_CONNS = 0x000400
PK_LOG_BE_DATA = 0x001000
PK_LOG_BE_HEADERS = 0x002000
PK_LOG_BE_CONNS = 0x004000
PK_LOG_MANAGER_ERROR = 0x010000
PK_LOG_MANAGER_INFO = 0x020000
PK_LOG_MANAGER_DEBUG = 0x040000
PK_LOG_TRACE = 0x080000
PK_LOG_LUA_DEBUG = 0x008000
PK_LOG_LUA_INFO = 0x000800
PK_LOG_ERROR = 0x100000
PK_LOG_ERRORS = (PK_LOG_ERROR|PK_LOG_MANAGER_ERROR)
PK_LOG_MANAGER = (PK_LOG_MANAGER_ERROR|PK_LOG_MANAGER_INFO)
PK_LOG_CONNS = (PK_LOG_BE_CONNS|PK_LOG_TUNNEL_CONNS)
PK_LOG_NORMAL = (PK_LOG_ERRORS|PK_LOG_CONNS|PK_LOG_MANAGER|PK_LOG_LUA_INFO)
PK_LOG_DEBUG = (PK_LOG_NORMAL|PK_LOG_MANAGER_DEBUG|PK_LOG_LUA_DEBUG)
PK_LOG_ALL = 0xffff00


def get_libpagekite_cdll():
    """Fetch a fully configured ctypes.cdll object for libpagekite."""
    from ctypes import cdll, c_void_p, c_char_p, c_int
    dll = cdll.LoadLibrary("libpagekite.so")
    for restype, func_name, argtypes in (
            (c_void_p, "init", (c_char_p, c_int, c_int, c_int, c_char_p, c_int, c_int,)),
            (c_void_p, "init_pagekitenet", (c_char_p, c_int, c_int, c_int, c_int,)),
            (c_void_p, "init_whitelabel", (c_char_p, c_int, c_int, c_int, c_int, c_char_p,)),
            (c_int, "add_kite", (c_void_p, c_char_p, c_char_p, c_int, c_char_p, c_char_p, c_int,)),
            (c_int, "add_service_frontends", (c_void_p, c_int,)),
            (c_int, "add_whitelabel_frontends", (c_void_p, c_int, c_char_p,)),
            (c_int, "lookup_and_add_frontend", (c_void_p, c_char_p, c_int, c_int,)),
            (c_int, "add_frontend", (c_void_p, c_char_p, c_int,)),
            (c_int, "set_log_mask", (c_void_p, c_int,)),
            (c_int, "set_housekeeping_min_interval", (c_void_p, c_int,)),
            (c_int, "set_housekeeping_max_interval", (c_void_p, c_int,)),
            (c_int, "enable_http_forwarding_headers", (c_void_p, c_int,)),
            (c_int, "enable_fake_ping", (c_void_p, c_int,)),
            (c_int, "enable_watchdog", (c_void_p, c_int,)),
            (c_int, "enable_tick_timer", (c_void_p, c_int,)),
            (c_int, "set_conn_eviction_idle_s", (c_void_p, c_int,)),
            (c_int, "want_spare_frontends", (c_void_p, c_int,)),
            (c_int, "thread_start", (c_void_p,)),
            (c_int, "thread_wait", (c_void_p,)),
            (c_int, "thread_stop", (c_void_p,)),
            (c_int, "free", (c_void_p,)),
            (c_int, "get_status", (c_void_p,)),
            (c_char_p, "get_log", (c_void_p,)),
            (c_int, "poll", (c_void_p, c_int,)),
            (c_int, "tick", (c_void_p,)),
            (c_int, "set_bail_on_errors", (c_void_p, c_int,))):
        method = getattr(dll, "pagekite_%s" % func_name)
        method.restype = restype
        method.argtypes = argtypes
    return dll


class PageKite(object):
    def __init__(self):
        self.dll = dll = get_libpagekite_cdll()
        self.pkm = pkm = None
        def cleanup():
            try:
                pkm.thread_stop()
                pkm.free()
            except (AssertionError, AttributeError):
                pass
        setattr(self, "cleanup", cleanup)
        setattr(self, "__del__", cleanup)

    def __exit__(self, *args): return self.cleanup()
    def __enter__(self): return self

    def init(self, *args):
        """
        Initialize the PageKite manager.
        
        This allocates a static amount of RAM for PageKite (not
        counting buffers managed by OpenSSL). Since libpagekite's
        resource usage is allocated up-front, you need to specify
        maximum numbers of kites, front-end relays and in-flight
        connections you want to keep track of at any one time.
        
        The `flags` variable should be used with the constants
        `PK_WITH_*` and `PK_AS_*`, bitwise OR'ed together to tune
        the behaviour of libpagekite. To use the recommended defaults,
        simply specify `PK_WITH_DEFAULTS`. Requesting defaults
        is a forward compatible choice and will continue to use
        recommended settings even as new features are added to
        the library.
        
        The `verbosity` argument controls the internal logging.
        A small integer (-1, 0, 1, 2) can be used to choose from
        a predefined level, for more fine-grained control use
        the `PK_LOG_` constants bitwise OR'ed together to enable
        logging of individual subsystems.
        
        This method can only be called before starting the master
        thread.
    
        Args:
           * `const char* app_id`: Short ID, reported in instrumentation
           * `int max_kites`: Max number of kite names allowed
           * `int max_frontends`: Max number of front-end relays recognized
           * `int max_conns`: Max number of in-flight connections
           * `const char* dyndns_url`: Dynamic DNS update URL (format string)
           * `int flags`: Flags, which features to enable
           * `int verbosity`: Verbosity or log mask
    
        Returns:
            The PageKite object on success, None otherwise
        """
        assert(self.pkm is None)
        self.pkm = self.dll.pagekite_init(*args)
        return (self if (self.pkm) else None)

    def init_pagekitenet(self, *args):
        """
        Initialize the PageKite manager, configured for use with
        the pagekite.net public service.
        
        See the basic init docs for further details.
        
        If `flags` do not include `PK_WITHOUT_SERVICE_FRONTENDS`,
        service frontends will be chosen automatically using the
        given domain name.
        
        This method can only be called before starting the master
        thread.
    
        Args:
           * `const char* app_id`: Short ID, reported in instrumentation
           * `int max_kites`: Max number of kite names allowed
           * `int max_conns`: Max number of in-flight connections
           * `int flags`: Flags, which features to enable
           * `int verbosity`: Verbosity or log mask
    
        Returns:
            The PageKite object on success, None otherwise
        """
        assert(self.pkm is None)
        self.pkm = self.dll.pagekite_init_pagekitenet(*args)
        return (self if (self.pkm) else None)

    def init_whitelabel(self, *args):
        """
        Initialize the PageKite manager, configured for use with
        a pagekite.net white-label domain.
        
        See the basic init docs for further details.
        
        If `flags` do not include `PK_WITHOUT_SERVICE_FRONTENDS`,
        white-label frontends will be chosen automatically using
        the given domain name.
        
        This method can only be called before starting the master
        thread.
    
        Args:
           * `const char* app_id`: Short ID, reported in instrumentation
           * `int max_kites`: Max number of kite names allowed
           * `int max_conns`: Max number of in-flight connections
           * `int flags`: Flags, which features to enable
           * `int verbosity`: Verbosity or log mask
           * `const char* whitelabel_tld`: Top level domain of white-label kites
    
        Returns:
            The PageKite object on success, None otherwise
        """
        assert(self.pkm is None)
        self.pkm = self.dll.pagekite_init_whitelabel(*args)
        return (self if (self.pkm) else None)

    def add_kite(self, *args):
        """
        Configure a "kite", mapping a public domain to a local
        service.
        
        Multiple kites can be configured for the same domain name,
        by calling this function multiple times, as long as the
        public port or protocol differ.
        
        This method can only be called before starting the master
        thread.
    
        Args:
           * `const char* proto`: Protocol
           * `const char* kitename`: Kite DNS name
           * `int pport`: Public port, 0 for default/any
           * `const char* secret`: Kite secret for authentication
           * `const char* backend`: Hostname of the origin server
           * `int lport`: Port of the origin server
    
        Returns:
            0 on success, -1 on failure.
        """
        assert(self.pkm is not None)
        return self.dll.pagekite_add_kite(self.pkm, *args)

    def add_service_frontends(self, *args):
        """
        Configure libpagekite to use the Pagekite.net pool of
        public front-end relay servers.
        
        This method can only be called before starting the master
        thread.
    
        Args:
           * `int flags`: Flags to enable IPv4, IPv6 and/or dynamic frontends
    
        Returns:
            The number of relay IPs configured, or -1 on failure.
        """
        assert(self.pkm is not None)
        return self.dll.pagekite_add_service_frontends(self.pkm, *args)

    def add_whitelabel_frontends(self, *args):
        """
        Configure libpagekite to use the relays associated with
        a Pagekite.net white-label domain.
        
        This method can only be called before starting the master
        thread.
    
        Args:
           * `int flags`: Flags to enable IPv4, IPv6 and/or dynamic frontends
           * `const char* whitelabel_tld`: Top level domain of white-label kites
    
        Returns:
            The number of relay IPs configured, or -1 on failure.
        """
        assert(self.pkm is not None)
        return self.dll.pagekite_add_whitelabel_frontends(self.pkm, *args)

    def lookup_and_add_frontend(self, *args):
        """
        Configure libpagekite front-end relays.
        
        All available IP addresses referenced by the specified
        DNS name will be configured as potential relays, and the
        app will choose between them based on performance metrics.
        
        If `update_from_dns` is nonzero, DNS will be rechecked
        periodically for new relay IPs. Enabling such updates
        is generally preferred over a completely static configuration,
        so long-running instances can keep up with changes to
        the relay infrastructure.
        
        This method can only be called before starting the master
        thread.
    
        Args:
           * `const char* domain`: DNS name of the frontend (or pool of frontends)
           * `int port`: Port to connect to
           * `int update_from_dns`: Set nonzero to re-lookup periodically from DNS
    
        Returns:
            The number of relay IPs configured, or -1 on failure.
        """
        assert(self.pkm is not None)
        return self.dll.pagekite_lookup_and_add_frontend(self.pkm, *args)

    def add_frontend(self, *args):
        """
        Configure libpagekite front-end relays.
        
        All available IP addresses referenced by the specified
        DNS name will be configured as potential relays, and the
        app will choose between them based on performance metrics.
        
        This method is static - DNS is only checked on startup.
        This is not optimal and this method is only provided for
        backwards compatibility. New apps should enable periodic
        DNS updates.
        
        This method can only be called before starting the master
        thread.
    
        Args:
           * `const char* domain`: DNS name of the frontend (or pool of frontends)
           * `int port`: Port to connect to
    
        Returns:
            The number of relay IPs configured, or -1 on failure.
        """
        assert(self.pkm is not None)
        return self.dll.pagekite_add_frontend(self.pkm, *args)

    def set_log_mask(self, *args):
        """
        Configure the log verbosity using a bitmask.
        
        See the `PK_LOG_*` constants for options.
        
        This function can be called at any time.
    
        Args:
           * `int mask`: A bitmask
    
        Returns:
            Always returns 0.
        """
        assert(self.pkm is not None)
        return self.dll.pagekite_set_log_mask(self.pkm, *args)

    def set_housekeeping_min_interval(self, *args):
        """
        Configure the minimum interval for internal housekeeping.
        
        Internal housekeeping includes attempting to re-establish
        a connection to the required relays, occasionally refreshing
        information from DNS and pinging tunnels to detect whether
        they have gone silently dead (due to NAT timeouts, for
        example).
        
        Setting this interval too low may reduce battery life
        or increase load on shared infrastructure, as a result
        there is a hard-coded minimum value which this function
        cannot override. Setting this interval too high may prevent
        libpagekite from detecting network outages and recovering
        in a timely fashion.
        
        The app will by default choose an interval between the
        minimum and maximum as appropriate. Most apps will not
        need to change this setting.
        
        This function can be called at any time.
    
        Args:
           * `int interval`: Interval, in seconds
    
        Returns:
            The new minimum housekeeping interval.
        """
        assert(self.pkm is not None)
        return self.dll.pagekite_set_housekeeping_min_interval(self.pkm, *args)

    def set_housekeeping_max_interval(self, *args):
        """
        Configure the maximum interval for internal housekeeping.
        
        See the documentation for the minimum housekeeping interval
        for details and performance concerns.
        
        This function can be called at any time.
    
        Args:
           * `int interval`: Interval, in seconds
    
        Returns:
            The new maximum housekeeping interval.
        """
        assert(self.pkm is not None)
        return self.dll.pagekite_set_housekeeping_max_interval(self.pkm, *args)

    def enable_http_forwarding_headers(self, *args):
        """
        Enable or disable HTTP forwarding headers.
        
        When enabled, libpagekite will rewrite incoming HTTP headers
        to add information about the remote IP address and remote
        protocol.
        
        The `X-Forwarded-For` header will contain the IP address
        of the remote HTTP client, as reported by the front-end
        relay (probably in IPv6 notation).
        
        The `X-Forwarded-Proto` header will report whether the
        connection to the relay was HTTP or HTTPS. This can be
        detected and used to redirect or reject plain-text connections.
        
        **Limitations**: Headers are only added to the first request
        of a persistent HTTP/1.1 session. The data reported comes
        from the front-end relay and a malicious relay could provide
        false data.
        
        This function can be called at any time.
    
        Args:
           * `int enable`: 0 disables, any other value enables
    
        Returns:
            Always returns 0.
        """
        assert(self.pkm is not None)
        return self.dll.pagekite_enable_http_forwarding_headers(self.pkm, *args)

    def enable_fake_ping(self, *args):
        """
        Enable or disable fake pings.
        
        This is a debugging/testing option, which effectively
        randomizes which front-end relay is used and increases
        the frequency of migrations.
        
        This function can be called at any time.
    
        Args:
           * `int enable`: 0 disables, any other value enables
    
        Returns:
            Always returns 0.
        """
        assert(self.pkm is not None)
        return self.dll.pagekite_enable_fake_ping(self.pkm, *args)

    def enable_watchdog(self, *args):
        """
        Enable or disable watchdog.
        
        The watchdog is a thread which periodically checks if
        the main pagekite thread has locked up. If it thinks the
        app has locked up, it will cause a segmentation fault,
        which in turn will create a core dump for debugging (assuming
        ulimits allow).
        
        This method can only be called before starting the master
        thread.
    
        Args:
           * `int enable`: 0 disables, any other value enables
    
        Returns:
            Always returns 0.
        """
        assert(self.pkm is not None)
        return self.dll.pagekite_enable_watchdog(self.pkm, *args)

    def enable_tick_timer(self, *args):
        """
        Enable or disable tick event timer.
        
        This method can be used to toggle the tick event timer
        on or off (it is on by default). Apps may want to disable
        the timer for power saving reasons.
        
        If the timer is disabled, the tick method should be called
        instead when possible, to ensure that housekeeping takes
        place.
        
        This method may be called at any time, but may hang as
        it waits for the main event-loop lock.
    
        Args:
           * `int enable`: 0 disables, any other value enables
    
        Returns:
            Always returns 0.
        """
        assert(self.pkm is not None)
        return self.dll.pagekite_enable_tick_timer(self.pkm, *args)

    def set_conn_eviction_idle_s(self, *args):
        """
        Configure eviction of idle connections.
        
        As libpagekite works with a fixed pool of RAM, it may
        be unable to allocate buffers for new incoming connections.
        When this happens, the oldest connection which has been
        idle for more than `seconds` seconds may be evicted.
        
        Set `seconds = 0` to disable eviction and instead reject
        incoming connections when overloaded. Eviction is disabled
        by default.
        
        This function can be called at any time.
    
        Args:
           * `int seconds`: Minimum idle time to qualify for eviction
    
        Returns:
            Always returns 0.
        """
        assert(self.pkm is not None)
        return self.dll.pagekite_set_conn_eviction_idle_s(self.pkm, *args)

    def want_spare_frontends(self, *args):
        """
        Connect to multiple front-end relays.
        
        If non-zero, this setting will configure how many spare
        relays to connect to at any given time. This may increase
        availability or performance in some special cases, but
        increases the load on shared relay infrastructure and
        should be avoided if possible.
        
        This function can be called at any time.
    
        Args:
           * `int spares`: Number of spare front-ends to connect to
    
        Returns:
            Always returns 0.
        """
        assert(self.pkm is not None)
        return self.dll.pagekite_want_spare_frontends(self.pkm, *args)

    def thread_start(self, *args):
        """
        Start the main thread: run pagekite!
        
        This function should only be called once (per session).
    
        Returns:
            The return value of `pthread_create()`
        """
        assert(self.pkm is not None)
        return self.dll.pagekite_thread_start(self.pkm, *args)

    def thread_wait(self, *args):
        """
        Wait for the main pagekite thread to finish.
        
        This function should only be called once (per session).
    
        Returns:
            The return value of `pthread_join()`
        """
        assert(self.pkm is not None)
        return self.dll.pagekite_thread_wait(self.pkm, *args)

    def thread_stop(self, *args):
        """
        Stop the main pagekite thread.
        
        This function should only be called once (per session).
    
        Returns:
            The return value of `pthread_join()`
        """
        assert(self.pkm is not None)
        return self.dll.pagekite_thread_stop(self.pkm, *args)

    def free(self, *args):
        """
        Free the internal libpagekite buffers.
        
        Call this to free any memory allocated by the init functions.
    
        Returns:
            0 on success, -1 on failure.
        """
        assert(self.pkm is not None)
        return self.dll.pagekite_free(self.pkm, *args)

    def get_status(self, *args):
        """
        Get the current status of the app.
        
        This function can be called at any time.
    
        Returns:
            A `PK_STATUS_*` code.
        """
        assert(self.pkm is not None)
        return self.dll.pagekite_get_status(self.pkm, *args)

    def get_log(self, *args):
        """
        Fetch the in-memory log buffer.
        
        Note that the C-API version returns a pointer to a static
        buffer. Subsequent calls will overwrite with new data.
        
        This function can be called at any time.
    
        Returns:
            A snapshot of the current log status.
        """
        assert(self.pkm is not None)
        return self.dll.pagekite_get_log(self.pkm, *args)

    def poll(self, *args):
        """
        Wait for the pagekite event loop to wake up.
        
        This method can be used to pause a thread, waking up again
        when libpagekite status changes, network activity takes
        place or other events take place which might affect the
        log or state variable.
        
        This method can be called any time the main thread is
        running.
    
        Args:
           * `int timeout`: Max time to wait, in seconds
    
        Returns:
            0 on success, -1 if unconfigured.
        """
        assert(self.pkm is not None)
        return self.dll.pagekite_poll(self.pkm, *args)

    def tick(self, *args):
        """
        Manually trigger the internal tick event.
        
        The internal tick event may trigger housekeeping if necessary.
        
        This method is only needed if the internal periodic timer
        has been disabled (e.g. on a mobile app, to conserve battery
        life).
        
        This method can be called any time the main thread is
        running.
    
        Returns:
            0 on success, -1 if unconfigured.
        """
        assert(self.pkm is not None)
        return self.dll.pagekite_tick(self.pkm, *args)

    def set_bail_on_errors(self, *args):
        """
        Enable or disable bailing out on errors.
        
        If enabled, the app will increase log verbosity and finally
        call `exit(100)` after too many errors have occurred.
        This can help catch and handle error states, but care
        should be taken as it will also bring down the hosting
        app.
        
        The sensitivity of this function depends on the `errors`
        variable. After `errors * 9` problems would have been
        logged, verbosity is increased. After `errors * 10`, the
        app will exit.
        
        This function can be called at any time.
    
        Args:
           * `int errors`: An error threshold
    
        Returns:
            Always returns 0.
        """
        assert(self.pkm is not None)
        return self.dll.pagekite_set_bail_on_errors(self.pkm, *args)
