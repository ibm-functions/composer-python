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

def generateEvenNumber(args):
    import random

    number = random.randint(0, 9)
    print('generated number {}'.format(number))

    if number % 2 != 0:
        raise Exception('error: number is not even')

    return { 'value': number }

def evenFailed(args):
    print('handling error, using default value')
    return { 'value': 42 }

def main():
    return composer.do(
      composer.retry(2, composer.action('generateEvenNumber', { 'action': generateEvenNumber })),
      composer.action('evenFailed', { 'action': evenFailed })
    )
