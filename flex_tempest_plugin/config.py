# Copyright 2015
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from oslo_config import cfg


KeyManagerOpts = [
    cfg.StrOpt('min_microversion',
               default=None,
               help="Lower version of the test target microversion range. "),
    cfg.StrOpt('max_microversion',
               default=None,
               help="Upper version of the test target microversion range. "),
    cfg.StrOpt('region',
               default='regionOne',
               help="The region name to use. If no such region is")
]