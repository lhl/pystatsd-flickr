#!/usr/bin/perl

use Flickr::StatsD::Quartiles;

$statsd = Flickr::StatsD::Quartiles->new();
$statsd->run_server();
