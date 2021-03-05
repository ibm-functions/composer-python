"""
 Licensed to the Apache Software Foundation (ASF) under one or more
 contributor license agreements.  See the NOTICE file distributed with
 this work for additional information regarding copyright ownership.
 The ASF licenses this file to You under the Apache License, Version 2.0
 (the "License"); you may not use this file except in compliance with
 the License.  You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""
import composer

def authenticate(args):
    return {'value': args['password'] == 'abc123'}

def success(args):
    return {'message': 'success'}

def failure(args):
    return {'message': 'failure'}

def main():
    return composer.when(
        composer.action('authenticate',  { 'action': authenticate }),
        composer.action('success', { 'action': success }),
        composer.action('failure', { 'action': failure }))
