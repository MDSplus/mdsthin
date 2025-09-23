#
# Copyright (c) 2025, Massachusetts Institute of Technology All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# Redistributions in binary form must reproduce the above copyright notice, this
# list of conditions and the following disclaimer in the documentation and/or
# other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

import os

from ..connection import *
from ..internals.usagedef import *

# TODO: Improve
_default_connection = None

def getDefaultConnection():
    global _default_connection
    if _default_connection is None:
        if 'MDS_HOST' in os.environ:
            _default_connection = Connection(os.environ['MDS_HOST'])
    return _default_connection

def setDefaultConnection(conn):
    global _default_connection
    _default_connection = conn

class _NCI:

    # Must be implemented
    def _getNci(self, property):
        raise Exception('_getNci must be implemented to subclass _NCI')

    # TODO: _setNci

    ###
    ### Flags
    ###

    @property
    def cached(self):
        return self._getNci('CACHED')

    # TODO: Add to MDSplus
    def isCached(self):
        return self.cached
    

    @property
    def compress_segments(self):
        return self._getNci('COMPRESS_SEGMENTS')

    def isCompressSegments(self):
        return self.compress_segments
    

    @property
    def compressible(self):
        return self._getNci('COMPRESSIBLE')
    
    def isCompressible(self):
        return self.compressible


    @property
    def essential(self):
        return self._getNci('ESSENTIAL')
    
    def isEssential(self):
        return self.essential


    @property
    def do_not_compress(self):
        return self._getNci('DO_NOT_COMPRESS')
    
    def isDoNotCompress(self):
        return self.do_not_compress


    @property
    def compress_on_put(self):
        return self._getNci('COMPRESS_ON_PUT')
    
    def isCompressOnPut(self):
        return self.compress_on_put


    @property
    def include_in_pulse(self):
        return self._getNci('INCLUDE_IN_PULSE')
    
    def isIncludeInPulse(self):
        return self.include_in_pulse


    @property
    def nid_reference(self):
        return self._getNci('NID_REFERENCE')
    
    # TODO: Add to MDSplus
    def isNidReference(self):
        return self._nid_reference


    @property
    def no_write_model(self):
        return self._getNci('NO_WRITE_MODEL')
    
    def isNoWriteModel(self):
        return self.no_write_model


    @property
    def no_write_shot(self):
        return self._getNci('NO_WRITE_SHOT')
    
    def isNoWriteShot(self):
        return self.no_write_shot


    @property
    def parent_state(self):
        return self._getNci('PARENT_STATE')
    
    # TODO: Add to MDSplus
    def getParentState(self):
        return self.parent_state


    @property
    def path_reference(self):
        return self._getNci('PATH_REFERENCE')
    
    def hasPathReferences(self):
        return self.path_reference


    @property
    def segmented(self):
        return self._getNci('SEGMENTED')
    
    def isSegmented(self):
        return self.segmented


    @property
    def setup_information(self):
        return self._getNci('SETUP_INFORMATION')
    
    # TODO: Add to MDSplus
    def hasSetupInformation(self):
        return self.setup_information
    

    @property
    def state(self):
        return self._getNci('STATE')
    
    # TODO: Add to MDSplus
    def getState(self):
        return self.state


    @property
    def versions(self):
        return self._getNci('VERSIONS')
    
    def containsVersions(self):
        return self.versions
    

    @property
    def write_once(self):
        return self._getNci('WRITE_ONCE')

    def isWriteOnce(self):
        return self.write_once
    
    ###
    ### Properties
    ###
    
    # set_flags
    # clear_flags

    @property
    def brother(self):
        nid = self._getNci('BROTHER')
        return TreeNode(nid, self._tree)
    
    def getBrother(self):
        return self.brother


    @property
    def child(self):
        nid = self._getNci('CHILD')
        return TreeNode(nid, self._tree)
    
    def getChild(self):
        return self.child


    @property
    def conglomerate_elt(self):
        return self._getNci('CONGLOMERATE_ELT')

    def getConglomerateElt(self):
        return self.getConglomerateElt()


    @property
    def conglomerate_nids(self):
        nids = self._getNci('CONGLOMERATE_NIDS')
        return TreeNodeArray(nids, self._tree)
    
    def getConglomerateNids(self):
        return self.conglomerate_nids


    @property
    def data_in_nci(self):
        return self._getNci('DATA_IN_NCI')
    
    # TODO: Add to MDSplus
    def hasDataInNci(self):
        return self.data_in_nci


    @property
    def depth(self):
        return self._getNci('DEPTH')
    
    def getDepth(self):
        return self.depth


    @property
    def dtype(self):
        return self._getNci('DTYPE')
    
    def getDtype(self):
        return self.dtype


    @property
    def dtype_str(self):
        return self._getNci('DTYPE_STR')
    
    def getDtypeStr(self):
        return self.dtype_str


    @property
    def error_on_put(self):
        return self._getNci('ERROR_ON_PUT')
    
    # TODO: Add to MDSplus
    def getErrorOnPut(self):
        return self.error_on_put
    

    @property
    def fullpath(self):
        return self._getNci('FULLPATH')
    
    def getFullPath(self):
        return self.fullpath


    @property
    def get_flags(self):
        return self._getNci('GET_FLAGS')
    
    def getFlags(self):
        return self.get_flags


    @property
    def length(self):
        return self._getNci('LENGTH')

    def getLength(self):
        return self.length


    @property
    def mclass(self):
        return self._getNci('CLASS')
    
    @property
    def class_str(self):
        return self._getNci('CLASS_STR')

    # TODO: Change in MDSplus to return self.mclass
    def getClass(self):
        return self.class_str
    
    # TODO: Add to MDSplus
    def getClassStr(self):
        return self.class_str


    @property
    def member(self):
        nid = self._getNci('MEMBER')
        return TreeNode(nid, self._tree)

    def getMember(self):
        return self.member


    @property
    def minpath(self):
        return self._getNci('MINPATH')

    def getMinPath(self):
        return self.minpath


    @property
    def node_name(self):
        return self._getNci('NODE_NAME')

    @property
    def name(self):
        return self.node_name

    def getNodeName(self):
        return self.node_name


    @property
    def number_of_children(self):
        return self._getNci('NUMBER_OF_CHILDREN')

    def getNumChildren(self):
        return self.number_of_children


    @property
    def number_of_elts(self):
        return self._getNci('NUMBER_OF_ELTS')

    def getNumElts(self):
        return self.number_of_elts
    
    # TODO: Rename in MDSplus?
    # def getNumElements(self):
    #     return self.number_of_elts


    @property
    def number_of_members(self):
        return self._getNci('NUMBER_OF_MEMBERS')

    def getNumMembers(self):
        return self.number_of_members


    @property
    def original_part_name(self):
        return self._getNci('ORIGINAL_PART_NAME')

    def getOriginalPartName(self):
        return self.original_part_name


    @property
    def parent(self):
        nid = self._getNci('PARENT')
        return TreeNode(nid, self._tree)

    def getParent(self):
        return self.parent


    @property
    def parent_relationship(self):
        return self._getNci('PARENT_RELATIONSHIP')

    # TODO: Add to MDSplus
    def getParentRelationship(self):
        return self.parent_relationship
    
    def isChild(self):
        return self.parent_relationship == 1

    def isMember(self):
        return self.parent_relationship == 2


    @property
    def on(self): # TODO: Setter
        return (int(self.get_flags) & 3) == 0

    def isOn(self):
        return self.on
    

    @property
    def disabled(self): # TODO: Setter
        return not self.on
    
    def isDisabled(self):
        return self.disabled
    

    @property
    def parent_on(self): # TODO: Setter
        return (int(self.get_flags) & 2) == 0

    def isParentOn(self):
        return self.parent_on
    

    @property
    def parent_disabled(self): # TODO: Setter
        return not self.parent_on
    
    def isParentDisabled(self):
        return self.parent_disabled


    @property
    def rfa(self):
        return self._getNci('RFA')

    # def getRfa(self):
    #     return self.rfa


    @property
    def rlength(self):
        return self._getNci('RLENGTH')

    def getCompressedLength(self):
        return self.rlength
    

    @property
    def status(self):
        return self._getNci('STATUS')

    def getStatus(self):
        return self.status
    

    def getTimeInserted(self):
        return self._getNci('TIME_INSERTED')
    
    @property
    def time_inserted(self):
        return self.getTimeInserted()
    

    @property
    def usage_str(self):
        return self._getNci('USAGE_STR')

    def getUsageStr(self):
        return self.usage_str


    @property
    def compression_method(self):
        return self._getNci('COMPRESSION_METHOD')

    # TODO: Add to MDSplus
    def getCompressionMethod(self):
        return self.compression_method


    @property
    def compression_method_str(self):
        return self._getNci('COMPRESSION_METHOD_STR')

    # TODO: Add to MDSplus
    def getCompressionMethodStr(self):
        return self.compression_method_str


# TODO:
class TreeNodeArray(_NCI):
    def __init__(self, nids, tree):
        self._conn = tree._conn
        self._tree = tree

        # TODO: Improve?
        self._nids = numpy.array(nids, dtype='int32')
    
    # __eq__

    def __getitem__(self, index):
        return TreeNode(self._nids[index], self._tree)

    # __len__

    # __add__

    def _getNci(self, property):
        return self._conn.get(f'getnci($,"{property}")', self._nids).data()

    @property
    def nid_number(self):
        return self._nids


    # TODO: Add to MDSplus
    def getTimeInsertedUnix(self):
        from datetime import datetime, timezone
        VMS_EPOCH = datetime.datetime(year=1858, month=11, day=17, tzinfo=timezone.utc)

        timestamps = self.getTimeInserted()
        for i in range(len(timestamps)):
            if timestamps[i] > 0:
                # From 100ns clunks to seconds
                timestamps[i] = (timestamps[i] * 100) / float(1e9)

                # Offset from VMS Epoch to UNIX Epoch
                timestamps[i] += VMS_EPOCH.timestamp()
        
        return timestamps
    
    # TODO: Add to MDSplus
    @property
    def time_inserted_unix(self):
        return self.getTimeInsertedUnix()

class TreeNode(_NCI):

    def __init__(self, nid, tree):
        self._conn: Connection = tree._conn
        self._tree: Tree = tree

        if type(nid) is str:
            self._nid = self._conn.get('getnci($,"NID_NUMBER")', nid.strip()).data()
        else:
            self._nid = numpy.int32(nid)

    def __repr__(self):
        return self.minpath
    
    def _getNci(self, property):
        return self._conn.get(f'getnci($,"{property}")', self._nid).data()
    

    # TODO: Add to MDSplus
    def getTimeInsertedUnix(self):
        from datetime import datetime, timezone
        VMS_EPOCH = datetime.datetime(year=1858, month=11, day=17, tzinfo=timezone.utc)

        timestamp = self.getTimeInserted()
        if timestamp > 0:
            # From 100ns clunks to seconds
            timestamp = (timestamp * 100) / float(1e9)

            # Offset from VMS Epoch to UNIX Epoch
            timestamp += VMS_EPOCH.timestamp()
        
        return timestamp
    
    # TODO: Add to MDSplus
    @property
    def time_inserted_unix(self):
        return self.getTimeInsertedUnix()


    @property
    def __children_nids(self):
        nids = self._conn.get('getnci(getnci($,"CHILDREN_NIDS"),"NID_NUMBER")', self._nid).data()
        return TreeNodeArray(nids, self._tree)

    @property
    def children_nids(self):
        try:
            return self.__children_nids
        except TreeNNF:
            return TreeNodeArray([], self._tree)

    def getChildren(self):
        return self.children_nids


    @property
    def __member_nids(self):
        nids = self._conn.get('getnci(getnci($,"MEMBER_NIDS"),"NID_NUMBER")', self._nid).data()
        return TreeNodeArray(nids, self._tree)

    @property
    def member_nids(self):
        try:
            return self.__member_nids
        except TreeNNF:
            return TreeNodeArray([], self._tree)

    def getMembers(self):
        return self.member_nids
    

    @property
    def number_of_descendants(self):
        return self._conn.get('getnci($,"NUMBER_OF_CHILDREN")+getnci($,"NUMBER_OF_MEMBERS")', self._nid, self._nid).data()
    
    def getNumDescendants(self):
        return self.number_of_descendants
    

    @property
    def descendants(self):
        # return self._conn.get(
        #     'set_range(size(_list), _list=[' +
        #         'getnci(getnci($,"CHILDREN_NIDS"),"NID_NUMBER"),' +
        #         'getnci(getnci($,"MEMBER_NIDS"),"NID_NUMBER")' +
        #     '])',
        #     self._nid, self._nid
        # ).data()

        gm = self._conn.getMany()
        gm.append('children', 'getnci(getnci($,"CHILDREN_NIDS"),"NID_NUMBER")', self._nid)
        gm.append('members', 'getnci(getnci($,"MEMBER_NIDS"),"NID_NUMBER")', self._nid)
        gm.execute()

        nids = []

        try:
            nids.extend(gm.get('children').data().tolist())
        except TreeNNF:
            pass

        try:
            nids.extend(gm.get('members').data().tolist())
        except TreeNNF:
            pass

        return TreeNodeArray(nids, self._tree)
    
    def getDescendants(self):
        return self.descendants


    @property
    def tag(self): # TODO: Setter
        return self.tags

    @property
    def tags(self):
        tags = []
        while True:
            tag = self._conn.get('TreeFindNodeTags($)', self._nid).data()
            if tag is None:
                break
            tags.append(tag)
        return tags
    
    def getTags(self):
        return self.tags


    @property
    def tree(self):
        return self._tree
    
    def getTree(self):
        return self.tree
    

    @property
    def nid(self):
        return self._nid

    def getNid(self):
        return self.nid


    def __getattr__(self, name):
        if name == name.upper():
            if name[0] == '_':
                name = '\\' + name[1 : ]
            return self.getNode(name)

    def getNode(self, path):
        if not path.startswith('\\'):
            path = self.fullpath + ':' + path # TODO: Replace : with ^?
        return TreeNode(path, self._tree)
    
    # TODO: Implement TreeFindNodeWildRelative in TDI
    # def getNodeWild(self, wildcard: str, *usage: str):
    #     usage_mask = 0xFFFF
    #     if len(usage) > 0:
    #         try:
    #             usage_mask = 0
    #             for u in usage:
    #                 usage_mask |= 1 << usage_lookup(u.upper())
    #         except KeyError:
    #             raise Exception(f'Unknown usage {u}')

    #     nids = self._conn.get('TreeFindNodeWild($,$)', wildcard, usage_mask).data()
    #     return TreeNodeArray(nids, self._tree)

    def __dir__(self):

        gm = self._conn.getMany()
        gm.append('member_name_list', 'getnci(getnci($,"MEMBER_NIDS"),"NODE_NAME")', self._nid)
        gm.append('child_name_list', 'getnci(getnci($,"CHILDREN_NIDS"),"NODE_NAME")', self._nid)
        gm.execute()

        name_list = []

        try:
            name_list.extend(gm.get('member_name_list').data().tolist())
        except TreeNNF:
            pass

        try:
            name_list.extend(gm.get('child_name_list').data().tolist())
        except TreeNNF:
            pass

        return name_list

    def dir(self):

        gm = self._conn.getMany()
        gm.append('children_name_list', 'getnci(getnci($,"CHILDREN_NIDS"),"NODE_NAME")', self._nid)
        gm.append('children_usage_list', 'getnci(getnci($,"CHILDREN_NIDS"),"USAGE")', self._nid)
        gm.append('member_name_list', 'getnci(getnci($,"MEMBER_NIDS"),"NODE_NAME")', self._nid)
        gm.append('member_usage_list', 'getnci(getnci($,"MEMBER_NIDS"),"USAGE")', self._nid)
        gm.execute()

        try:
            children_name_list = gm.get('children_name_list').data().tolist()
            children_usage_list = gm.get('children_usage_list').data().tolist()

            for name, usage in zip(children_name_list, children_usage_list):
                print(f'{name:<15} {usage_to_name(usage)}')
                
        except TreeNNF:
            pass

        try:
            member_name_list = gm.get('member_name_list').data().tolist()
            member_usage_list = gm.get('member_usage_list').data().tolist()

            for name, usage in zip(member_name_list, member_usage_list):
                print(f'{name:<15} {usage_to_name(usage)}')

        except TreeNNF:
            pass

    @property
    def record(self):
        return self._conn.getObject(self.fullpath)

    def data(self):
        return self._conn.get(self.fullpath).data()

    def raw_of(self):
        return self._conn.get(f'raw_of({self.fullpath})')

    def dim_of(self):
        return self._conn.get(f'dim_of({self.fullpath})')

class classmethodX(object):
    def __get__(self, inst, cls):
        if inst is None:
            return self.method.__get__(cls)
        else:
            return self.method.__get__(inst)

    def __init__(self, method):
        self.method = method

class Tree(TreeNode):

    def __init__(self, tree: str, shot: int = -1, mode: str = 'NORMAL', path: str = None, conn: Connection = None):
        self._conn: Connection = conn
        if self._conn is None:
            self._conn = getDefaultConnection()
            if self._conn is None:
                raise Exception('Unable to create an mdsthin.Tree without a connection.')

        # TODO: Clone connection so that each Tree has its own Connection

        self._treename = tree
        self._path = path
        self.open(mode, shot)

        # TODO: Use 0, the default nid, or the nid of \\TOP ?
        super().__init__(self._conn.get('GetDefaultNid()'), self)
        # super().__init__(self, self._conn.get('getnci("\\\\TOP","NID_NUMBER")'))

    def __repr__(self):
        return f'Tree("{self._treename.upper()}",{self.shot},"Normal")'

    ###
    ### DBI Properties
    ###

    @property
    def name(self):
        return self._conn.get('getdbi("NAME")').data()

    @property
    def tree(self):
        return self.name

    # TODO: Add to MDSplus
    def getName(self):
        return self.name


    @property
    def shotid(self):
        return self._conn.get('getdbi("SHOTID")').data()

    @property
    def shot(self):
        return self.shotid
    
    # TODO: Add to MDSplus
    def getShot(self):
        return self.shotid


    @property
    def modified(self):
        return self._conn.get('getdbi("MODIFIED")').data()

    def isModified(self):
        return self.modified


    @property
    def open_for_edit(self):
        return self._conn.get('getdbi("OPEN_FOR_EDIT")').data()

    def isOpenForEdit(self):
        return self.open_for_edit
    

    @property
    def index(self):
        return self._conn.get('getdbi("INDEX")').data()

    # TODO: Add to MDSplus
    def getIndex(self):
        return self.index


    @property
    def number_opened(self):
        return self._conn.get('getdbi("NUMBER_OPENED")').data()
    
    def getNumOpened(self):
        return self.number_opened


    @property
    def max_open(self):
        return self._conn.get('getdbi("MAX_OPEN")').data()
    
    def getMaxOpen(self):
        return self.max_open


    @property
    def default(self):
        nid = self._conn.get('GetDefaultNid()')
        return TreeNode(nid, self)
    
    def getDefault(self):
        return self.default
    
    def setDefault(self, node: TreeNode | str | int | numpy.int32):
        if node is str:
            status = self.get('TreeSetDefault($)', node).data()
        else:
            if node is TreeNode:
                nid = node.nid
            else:
                nid = numpy.int32(nid)
            
            status = self.get('SetDefaultNid($)', nid)

        if STATUS_NOT_OK(status):
            raise getException(status)


    @property
    def open_readonly(self):
        return self._conn.get('getdbi("OPEN_READONLY")').data()
    
    def isReadOnly(self):
        return self.open_readonly


    @property
    def versions_in_model(self):
        return self._conn.get('getdbi("VERSIONS_IN_MODEL")').data()
    
    def versionsInModelEnabled(self):
        return self.versions_in_model


    @property
    def versions_in_pulse(self):
        return self._conn.get('getdbi("VERSIONS_IN_PULSE")').data()

    def versionsInPulseEnabled(self):
        return self.versions_in_pulse


    @property
    def dispatch_table(self):
        return self._conn.get('getdbi("DISPATCH_TABLE")').data()
    
    # TODO: Add to MDSplus
    def getDispatchTable(self):
        return self.dispatch_table


    @property
    def alternate_compression(self):
        return self._conn.get('getdbi("ALTERNATE_COMPRESSION")').data()

    # TODO: Add to MDSplus
    def alternateCompressionAllowed(self):
        return self.alternate_compression

    @property
    def top(self):
        return TreeNode(0, self)
    
    # TODO: Investigate
    @property
    def public(self):
        return False
    
    def copy(self):
        return Tree(
            tree=self._treename,
            shot=self._shot,
            mode=self._mode,
            path=self._path,
            conn=self._conn.copy()
        )

    def readonly(self, shot: int = None):
        self.open('READONLY', shot)

    def edit(self, shot: int = None):
        self.open('EDIT', shot)

    def normal(self, shot: int = None):
        self.open('NORMAL', shot)

    def open(self, mode: str = 'NORMAL', shot: int = None):
        if shot is not None:
            self._shot = shot

        try:
            env_name = f'{self._treename.lower()}_path'
            if self._path is not None:
                old_path = self._conn.get(f'getenv("{env_name}")')
                self._conn.get(f'setenv("{env_name}={self._path}")')

            self._mode = mode.upper()
            if self._mode == 'NORMAL':
                status = self._conn.get('TreeOpen($,$)', self._treename, self._shot).data()
            elif self._mode == 'EDIT':
                status = self._conn.get('TreeOpenEdit($,$)', self._treename, self._shot).data()
            elif self._mode == 'READONLY':
                status = self._conn.get('TreeOpen($,$,1)', self._treename, self._shot).data()
            # elif self._mode == 'NEW':
            #     status = self._conn.get('TreeOpenNew($,$)', self._treename, self._shot).data()
            else:
                raise TypeError('Invalid mode specificed, must be "readonly", "normal", "edit", or "new"')

            if STATUS_NOT_OK(status):
                raise getException(status)
            
        finally:
            if self._path is not None:
                self._conn.get(f'setenv("{env_name}={old_path}")')

    @classmethodX
    def setCurrent(self, tree: str = None, shot: int = None, conn: Connection = None):
        # TODO: Investigate
        if isinstance(self, Tree):
            shot = self._shot if tree is None else tree
            tree = self._treename
            conn = self._conn

        if conn is None:
            conn = getDefaultConnection()

            if conn is None:
                raise Exception('Unable to use mdsthin.Tree without a connection.')

        status = conn.get('TreeSetCurrentShot($,$)', tree, shot).data()

        if STATUS_NOT_OK(status):
            raise getException(status)
    
    def getCurrent(self, tree: str = None, conn: Connection = None):
        if isinstance(self, Tree):
            tree = self._treename
            conn = self._conn

        if conn is None:
            conn = getDefaultConnection()

            if conn is None:
                raise Exception('Unable to use mdsthin.Tree without a connection.')

        shot = conn.get('TreeGetCurrentShot($)', tree).data()
        if shot == 0:
            raise TreeNOCURRENT()
        
        return shot
