import os
import shotgun_api3
import royalRifle_entityConfig as entityConfig
import rrSG
import rrGlobal

class RoyalRifleException(Exception):
    """ This class will be used by the RoyalRifle class to define errors
    """
    def __init__(self, msg):
        rrGlobal.messageBox(rrGlobal.logLvL.warning, msg,"","", False,30)
        super(RoyalRifleException, self).__init__()


class RoyalRifle(object):
    """ This class holds an interface to Shotgun.
        Several methods in this class can be changed to change the bahaviour of RoyalRender within Shotgun.
        
        Terminology::
        
                entity = a node in shotgun (datatype is dict)
                renderEntity = entity in Shotgun to represent a render job
                jobEntity = renderEntity
                submitEntity = entity in Shotgun to represent a submission
                
                _sgAttrPrefix = prefix Shotgun uses to differ user-attributes from build-in attributes
        
        A short list of these callback-methods::
            
            #1) submitRender            creates entities in Shotgun representing each job and each submission
            #2) addPreviewImages        adds a list of images to renderEntities in Shotgun.
            #3) addQuicktime            adds preview quicktimes to renderEntities
            #4) sendNotification        sends a notification in Shotgun to the submitter
    """
    
    _sgAttrPrefix = 'sg_'
    
    sg = None
    
    def __init__(self):
        rrGlobal.writeLog(rrGlobal.logLvL.info, "RoyalRifle __init__", "RoyalRifle")
        self.sg=rrSG.rifleConnect()
        print(str(self.sg))
        

    def getAllTasks(self, projectName):
        """ method will return all tasks added to a project
            
            :param projectName: name of the project
            :type projectName: string
            
            :returns: a list of task-entities
            :rtype: list
        """
        return self.sg.find(
                        'Task',
                        filters = [['project', 'name_is', projectName]],
                        fields=self.sg.schema_field_read('Task').keys()
                )
    
    
    def getAllShots(self, projectName):
        """ method will return all shots added to a project
            
            :param projectName: name of the project
            :type projectName: string
            
            :returns: a list of all shots
            :rtype: tuple
        """
        allShots = self.sg.find(
                        'Shot',
                        filters = [['project', 'name_is', projectName]],
                        fields=self.sg.schema_field_read('Shot').keys()
                )
        
        return (allShots)
    
    def getShotEntity(self, renderEntityId):
        """ method will returnthe dictionary of the shot entity in Shotgun, which is linked to the given Shotgun-renderEntity
            
            :param renderEntityId: render entity id in shotgun
            :type renderEntityId: int
            
            :returns: the linked shot entity in shotgun
            :rtype: dict
        """
        
        # create shotgun entity instance
        submitEntity = self.getSubmitEntity(renderEntityId)
        
        allFields = self.sg.schema_field_read('Shot').keys()
        return self.sg.find_one('Shot', filters=[['id', 'is', submitEntity['%slinked_shot'%self._sgAttrPrefix]['id']]], fields=allFields)
    
    def getSubmitEntity(self, renderEntityId):
        """ method will returnthe dictionary of the submit entity in Shotgun, which is linked to the given renderEntity
            
            :param renderEntityId: render entity id in shotgun
            :type renderEntityId: int
            
            :returns: the linked submit entity in shotgun
            :rtype: dict
        """
        
        # create shotgun entity instance
        renderEntity = self._findRenderEntity(renderEntityId)
        submitEntity = self._findSubmitEntity(renderEntity['%slinked_submit_entity'%self._sgAttrPrefix]['id'])
        
        return submitEntity
    
    def getShotEntityFromRRJobId(self, rrJobId):
        """ method will returnthe dictionary of the shot entity in Shotgun, which is linked to the given royalRender job id
            
            :param rrJobId: render job id in Royal Render
            :type rrJobId: int
            
            :returns: the linked shot entity in shotgun
            :rtype: dict
        """
        
        # create shotgun entity instance
        submitEntity = self.getSubmitEntityFromRRJobId(rrJobId)
        
        allFields = self.sg.schema_field_read('Shot').keys()
        return self.sg.find_one('Shot', filters=[['id', 'is', submitEntity['%slinked_shot'%self._sgAttrPrefix]['id']]], fields=allFields)
    
    def getSubmitEntityFromRRJobId(self, rrJobId):
        """ method will returnthe dictionary of the submit entity in Shotgun, which is linked to the given royalRender job id
            
            :param rrJobId: render job id in Royal Render
            :type rrJobId: int
            
            :returns: the linked submit entity in shotgun
            :rtype: dict
        """
        
        # create shotgun entity instance
        renderEntity = self.getRenderEntityFromRRJobId(rrJobId)
        submitEntity = self._findSubmitEntity(renderEntity['%slinked_submit_entity'%self._sgAttrPrefix]['id'])
        
        return submitEntity
    
    def getRenderEntityFromRRJobId(self, rrJobId):
        """ method will returnthe dictionary of the render entity in Shotgun, which is linked to the given royalRender job id
            
            :param rrJobId: render job id in Royal Render
            :type rrJobId: int
            
            :returns: the shotgun render entity in shotgun
            :rtype: dict
        """
        
        # create shotgun entity instance
        minimalRenderEntity = self.sg.find_one(rrSG.entityJob(),
                        filters=[['%sjob_id'%self._sgAttrPrefix, 'is', rrJobId]])
        
        renderEntity = self._findRenderEntity(minimalRenderEntity['id'])
        
        return renderEntity
    
    def submitRender(self, renderDataList, submitUser, projectName, UNUSEDID, shotId, taskId=None):
        """ method will enter the current submission in shotgun. It will be called by the rrSubmitter.
            
            For each submission, this method will create one submit entity in shotgun and each render-pass/layer will get one
            render entity. All render entities will be linked to the submission entity while the submit entity is linked to the
            submitter, the shot, and, if given, the task::
                
                
                |_shot
                  |_SUBMIT-ENTITY ----------> submitter
                    |_RENDER-ENTITY-1
                    |_RENDER-ENTITY-..
                    |_RENDER-ENTITY-n
                
            
            :param renderDataList: this list holds dictionaries with attributes, which should be set to the render and submit entities.
                    as keys you can use any attribute listed in the config file and all default attribute names loke code, description etc
                    The containing values have to be in the correct data-type
            :type renderDataList: list
            :param submitUser: login-name of the submitter
            :type submitUser: string
            :param projectName: name of  the project the submission is containing to
            :type projectName: string
            :param shotId: id of the shot the submission is containing to
            :type shotId: string
            :param taskId: int of  the shot the submission is containing to (optional)
            :type taskId: int
            
            :returns: the created submit entity in shotgun
            :rtype: dict
        """
        
        
        # create shotgun entity instances
        project = self._findProject(projectName)
        user = self._findUser(submitUser)
        shot = self._findShot(shotId)
        if taskId:
            task = self._findTask(taskId)
        
        creationDict = {}
        creationDict['%slinked_shot'%self._sgAttrPrefix] = shot
        creationDict['%slinked_user'%self._sgAttrPrefix] = user
        if taskId:
            creationDict['%slinked_task'%self._sgAttrPrefix] = task
        creationDict['code'] = 'render_%s'%(shot['code'])
        creationDict['project'] = project
        
        submitEntity = self.sg.create(rrSG.entitySubmit(), creationDict, ['type', 'id', 'code'])
        
        renderJobEntities = []
        for i, renderData in enumerate(renderDataList):
            if not i:
                self.sg.update(
                                submitEntity['type'],
                                submitEntity['id'],
                                {
                                        '%srender_application'%self._sgAttrPrefix:renderData.get('render_application', ''),
                                        '%srender_scene_name'%self._sgAttrPrefix : {
                                                        'local_path' : renderData.get('render_scene_name', '')
                                                },
                                }
                        )
            
            renderJobEntities.append(self.addRenderJobEntities(submitEntity, project, renderData))
            self.sg.update(
                            renderJobEntities[-1]['type'],
                            renderJobEntities[-1]['id'],
                            {'%slinked_submit_entity'%self._sgAttrPrefix: submitEntity,}
                    )
        
        # link dependencies
        self.sg.update(
                        submitEntity['type'],
                        submitEntity['id'],
                        {'%slinked_jobs'%self._sgAttrPrefix : renderJobEntities}
                )
        
        self.sg.update(
                        shot['type'],
                        shot['id'],
                        {'%sroyal_render_watch'%self._sgAttrPrefix:[submitEntity]}
                )
        if taskId:
            self.sg.update(
                            task['type'],
                            task['id'],
                            {'%sroyal_render_watch'%self._sgAttrPrefix:[submitEntity]}
                    )
        
        return self._findSubmitEntity(submitEntity['id'])
    
    def addRenderJobEntities(self, submissionJob, project, renderData):
        """ method will add a render job entity. It will be called by submitRender.
            
            :param submissionJob: dictionary of the submit entity with at least 'type',  'id' and 'code' key
            :type submissionJob: dict
            :param project: dictionary of the project entity with at least 'type' and 'id' key
            :type project: dict
            :param renderData: dictionary with attributes, which should be set to the render and submit entities.
                    as keys you can use any attribute listed in the config file and all default attribute names loke code, description etc
                    The containing values have to be in the correct data-type
            :type renderData: dict
            
            :returns: the created render entity in shotgun
            :rtype: dict
        """
        
        creationDict = {}
        
        # debug and cleanup renderData dict
        if not renderData.has_key('job_id'):
            raise RoyalRifleException('renderData dictionary needs job_id value')
        
        if renderData.has_key('project'):
            renderData.pop('project')
        if renderData.has_key('shot'):
            renderData.pop('shot')
        if renderData.has_key('task'):
            renderData.pop('task')
        if renderData.has_key('code'):
            renderData.pop('code')
        
        description = renderData.get('description', '')
        
        # fill creationDict with correct values
        allEntityFieldNames = [each['name'] for each in entityConfig.jobEntityFields]
        for eachFieldName, eachFieldValue in renderData.items():
            if not eachFieldName in allEntityFieldNames:
                continue
            creationDict['%s%s'%(self._sgAttrPrefix, eachFieldName)] = eachFieldValue
        
        creationDict['project'] = project
        creationDict['code'] = '%s_%s'%(submissionJob['code'], renderData['job_id'])
        creationDict['description'] = description
        creationDict['%sstatus_list'%self._sgAttrPrefix] = 'wtg'
        
        # create new render entity
        renderEntity = self.sg.create(rrSG.entityJob(), creationDict, ['type', 'id', 'code'])
        
        return renderEntity
    
    
    def sendNotification(self, renderEntityId, renderMessageDict, addressedToSubmitter=True):
        """ method sends a notification to to the renderEntity and by default also to the submitter.
            
            :param renderEntityId: the entity id of the render entity in shotgun
            :type renderEntityId: int
            :param renderMessageDict: a dictionary with at least 'content' and 'subject' keys
            :type renderMessageDict: dict
            :param addressedToSubmitter: defines wether the note should be addressed to the submitter or not
            :type addressedToSubmitter: bool
            
            :returns: the note-entity created in shotgun
            :rtype: dict
        """
        
        # debug input arguments
        if not renderMessageDict.has_key('subject'):
            raise RoyalRifleException('renderMessageDict is missing a subject')
        if not renderMessageDict.has_key('content'):
            raise RoyalRifleException('renderMessageDict is missing a content')
        
        # get shotgun entity instances
        renderEntity = self._findRenderEntity(renderEntityId)
        submitEntity = self._findSubmitEntity(renderEntity['%slinked_submit_entity'%self._sgAttrPrefix]['id'])
        
        user = self.sg.find_one(
                        submitEntity['%slinked_user'%self._sgAttrPrefix]['type'],
                        filters=[['id', 'is', submitEntity['%slinked_user'%self._sgAttrPrefix]['id']]]
                )
        
        addressedTo = []
        if addressedToSubmitter:
            addressedTo = [submitEntity['%slinked_user'%self._sgAttrPrefix]]
        
        # create a note addressing to the submitter
        note = self.sg.create('Note', {
                                'addressings_to' : addressedTo,
                                'subject' : renderMessageDict['subject'],
                                'project' : renderEntity['project'],
                                'note_links' : [renderEntity],
                                'content': renderMessageDict['content']
                        }, ['type', 'id']
                )
        
        self.sg.update(
                        renderEntity['type'],
                        renderEntity['id'],
                        {'%sstatus_list'%self._sgAttrPrefix:'rev'}
                )
        self.setSubmitEntityState(submitEntity)
        return note
    
    def addPreviewImages(self, renderEntityId, imagePathList, approvalLink = ''):
        """ this method adds a given list of images to a render entity. If given an approvalLink, this will be added as link to the previews.
            Affter adding the images it will change the state of the render entity to review
            
            :param renderEntityId: the entity id of the render entity in shotgun
            :type renderEntityId: int
            :param imagePathList: a list of file paths(strings) pointing to the location of each preview image
            :type imagePathList: list
            :param approvalLink: an URL which can be used to approve the previews
            :type approvalLink: string
            
            :returns: None
            :rtype: None
        """
        
        # get shotgun entity instances
        renderEntity = self._findRenderEntity(renderEntityId)
        
        # debug input arguments
        if not len(imagePathList):
            raise RoyalRifleException('at least one image has to be given')
        
        approvalText=''
        if approvalLink:
            approvalText = 'press %s to approve' % approvalLink
        msgDict = {
                        'subject' : 'preview rendered',
                        'content' : 'please check the attached preview images\n%s'%approvalText
                }
        note = self.sendNotification(renderEntityId, msgDict, False)
        
        # configuration logic
        for i, eachPath in enumerate(imagePathList):
            if not os.path.exists(eachPath):
                continue
            # upload the first image as thumbnail to the renderEntity
            if not i:
                self.sg.upload_thumbnail(renderEntity['type'], renderEntity['id'], eachPath)
            
            self.sg.upload(
                            note['type'],
                            note['id'],
                            eachPath,
                    )
    
    def addQuicktime(self, renderEntityId, linkToQuicktime, pathToQuicktime=''):
        """ this method adds a new version to the render entity, which links to a local path of a quicktime. If a proxypath is given
            it will also upload this lowRes file to the shotgun dataBase.
            After adding the version the state of the render entity will be set to complete
            
            :param renderEntityId: the entity id of the render entity in shotgun
            :type renderEntityId: int
            :param linkToQuicktime: path to the highRes quicktime, which should be added as link to shotgun
            :type linkToQuicktime: string
            :param pathToQuicktime: path to the lowRes quicktime, which should be uploaded to shotgun
            :type pathToQuicktime: string
            
            :returns: created version entity
            :rtype: dict
        """
        
        if not os.path.exists(linkToQuicktime):
            raise RoyalRifleException('Path to quicktime not found! %s'%linkToQuicktime)
        
        # get shotgun entity instances
        renderEntity = self._findRenderEntity(renderEntityId)
        submitEntity = self._findSubmitEntity(renderEntity['%slinked_submit_entity'%self._sgAttrPrefix]['id'])
        
        shot = self.sg.find_one(
                        submitEntity['%slinked_shot'%self._sgAttrPrefix]['type'],
                        filters=[['id', 'is', submitEntity['%slinked_shot'%self._sgAttrPrefix]['id']]],
                        fields=['id', 'type', 'code', '%sversion'%self._sgAttrPrefix]
                )
        
        # create version
        data = { 'project': renderEntity['project'],
                 'code': '%s_qt_v1'%submitEntity['code'],
                 'description': renderEntity['%srender_pass'%self._sgAttrPrefix],
                 '%sstatus_list'%self._sgAttrPrefix: 'rev',
                 'entity': shot,
                 '%stask'%self._sgAttrPrefix: renderEntity,
                 'user': submitEntity['%slinked_user'%self._sgAttrPrefix]
            }
        version = self.sg.create('Version', data)
        
        if pathToQuicktime:
            if not os.path.exists(pathToQuicktime):
                print 'Path to quicktime not found! %s'%pathToQuicktime
            else:
                # upload quicktime
                self.sg.upload( version['type'],
                                version['id'],
                                pathToQuicktime,
                                field_name='%suploaded_movie'%self._sgAttrPrefix,
                                display_name='rendering_%s'%renderEntity['%sjob_id'%self._sgAttrPrefix],
                                tag_list='%s'%renderEntity['%sjob_id'%self._sgAttrPrefix]
                        )
        
        # link quicktime
        self.sg.update(
                        version['type'],
                        version['id'],
                        {
                                '%suploaded_movie'%self._sgAttrPrefix:{'local_path' : linkToQuicktime},
                                '%spath_to_movie'%self._sgAttrPrefix:linkToQuicktime
                        }
                )
        
        allVersions = shot['%sversion'%self._sgAttrPrefix]
        allVersions.append(version)
        
        # link version with shot
        self.sg.update(
                        shot['type'],
                        shot['id'],
                        {'%sversion'%self._sgAttrPrefix: allVersions}
                )
        
        self.sg.update(
                        renderEntity['type'],
                        renderEntity['id'],
                        {'%sstatus_list'%self._sgAttrPrefix:'cmpt'}
                )
        
        self.setSubmitEntityState(submitEntity)
        return version
    
    
    def _findProject(self, projectName):
        """ method will return a project in shotgun.
            
            :param projectName: name of the project to be returned
            :type projectName: string
            
            :returns: the found project entity
            :rtype: dict
        """
        
        project = self.sg.find_one('Project', filters=[['name', 'is', projectName]])
        if not project:
            raise RoyalRifleException("project '%s' is not in shotgun database!"%projectName)
        return project
    
    
    def _findShot(self, shotId):
        """ method will return a shot of a project in shotgun .
            
            :param shotId: id of the shot to be found
            :type shotId: string
            
            :returns: the found shot entity
            :rtype: dict
        """
        
        shot = self.sg.find_one(
                        'Shot',
                        filters=[['code', 'is', shotId]],
                        fields=['id', 'type', 'code', '%sversion'%self._sgAttrPrefix]
                        )
        if not shot:
            raise RoyalRifleException("shot '%s' not in shotgun database!"%shotId)
        return shot
    
    def _findTask(self, tskId):
        """ method will return a task of a project in shotgun .
            
            :param tskId: id of the task to be found
            :type tskId: int
            
            :returns: the found task entity
            :rtype: dict
        """
        
        tsk = self.sg.find_one(
                        'Task',
                        filters=[['name', 'is',tskId]]
                )
        if not tsk:
            raise RoyalRifleException('task %s not in shotgun database!'%tskId)
        return tsk
    
    def _findUser(self, userName):
        """ method will return a humanUser entity based on the given login name.
            
            :param userName: login name of the shotgun user
            :type userName: string
            
            :returns: the found humanUser entity
            :rtype: dict
        """
        
        usr = self.sg.find_one('HumanUser', filters=[['login', 'is', userName]])
        if not usr:
            raise RoyalRifleException('user %s not in shotgun database!'%userName)
        return usr
    
    def _findRenderEntity(self, id):
        """ method will returns the render entity with the given id.
            
            :param id: id of the render entity to be searched for
            :type id: int
            
            :returns: the found render entity with all attributes and their values in the dictionary
            :rtype: dict
        """
        
        fieldList = ['%s%s'%(self._sgAttrPrefix, each['name']) for each in entityConfig.jobEntityFields]
        fieldList.extend(['id', 'type', 'project', 'code', 'description'])
        
        renderEntity = self.sg.find_one(
                        rrSG.entityJob(),
                        filters=[['id', 'is', id]],
                        fields=fieldList
                    )
        
        if not renderEntity:
            raise RoyalRifleException('renderEntity %s not in shotgun database!'%id)
        return renderEntity

    def _updateRenderEntity(self, id, renderEntity):
        """ method will update the render entity with the given id.
            
            :param id: id of the render entity to be searched for
            :type id: int

            :param renderEntity: renderEntity retrieved with _findRenderEntity
            :type renderEntity: renderEntity
            
        """
        self.sg.update(
                        rrSG.entityJob(),
                        id,
                        renderEntity
                    )

    def setRenderEntityStateComplete(self, id):
        """ method changes the status of a render entity based on the current status
            
            status of a submit entity::
                
                'rev'       =       if all linked render entities are set to review
                'cmpt'      =       if all linked render entities are set to complete
                'ip'            =       in any other case
            
            :param submitEntity: submit entity in shotgun
            :type submitEntity: dict
            
            :returns: the state the submit entity has been set to.
            :rtype: string
        """
        
        state = 'cmpt'
        
        self.sg.update(
                        rrSG.entityJob(),
                        id,
                        {'%sstatus_list'%self._sgAttrPrefix:state}
                )
        return state

    def setRenderEntityState(self, id, newStatus):
        """ method changes the status of a render entity based on the current status
            
            status of a submit entity::
                
                'rev'       =       if all linked render entities are set to review
                'cmpt'      =       if all linked render entities are set to complete
                'ip'            =       in any other case
            
            :param submitEntity: submit entity in shotgun
            :type submitEntity: dict
            
            :returns: the state the submit entity has been set to.
            :rtype: string
        """
        
        self.sg.update(
                        rrSG.entityJob(),
                        id,
                        {'%sstatus_list'%self._sgAttrPrefix:newStatus}
                )
        return newStatus            
    
    def setSubmitEntityState(self, submitEntity):
        """ method changes the status of a submit entity based on the current status of all child render entities
            
            status of a submit entity::
                
                'rev'       =       if all linked render entities are set to review
                'cmpt'      =       if all linked render entities are set to complete
                'ip'            =       in any other case
            
            :param submitEntity: submit entity in shotgun
            :type submitEntity: dict
            
            :returns: the state the submit entity has been set to.
            :rtype: string
        """
        
        renderEntities = self.sg.find_one(
                        submitEntity['type'],
                        filters=[['id', 'is', submitEntity['id']]],
                        fields=['id', 'type', 'code', '%slinked_jobs'%self._sgAttrPrefix]
                )['%slinked_jobs'%self._sgAttrPrefix]
        
        done = []
        waiting = []
        
        for eachEntity in renderEntities:
            state = self.sg.find_one(
                            eachEntity['type'],
                            filters=[['id', 'is', eachEntity['id']]],
                            fields = ['%sstatus_list'%self._sgAttrPrefix]
                    )['%sstatus_list'%self._sgAttrPrefix]
            
            if state == 'cmpt':
                done.append(eachEntity)
            elif state == 'rev':
                waiting.append(eachEntity)
        
        state = 'ip'
        if len(done) == len(renderEntities):
            state = 'cmpt'
        elif len(waiting) == len(renderEntities):
            state = 'rev'
        
        self.sg.update(
                        submitEntity['type'],
                        submitEntity['id'],
                        {'%sstatus_list'%self._sgAttrPrefix:state}
                )
        return state
    
    def _findSubmitEntity(self, id):
        """ method will returns the submit entity with the given id.
            
            :param id: id of the submit entity to be searched for
            :type id: int
            
            :returns: the found submit entity with all attributes and their values in the dictionary
            :rtype: dict
        """
        
        fieldList = ['%s%s'%(self._sgAttrPrefix, each['name']) for each in entityConfig.submitEntityFields]
        fieldList.extend(['id', 'type', 'project', 'code', 'description'])
        
        renderEntity = self.sg.find_one(rrSG.entitySubmit(),
                        filters=[['id', 'is', id]],
                        fields=fieldList
                    )
        if not renderEntity:
            raise RoyalRifleException('submissionEntity %s not in database!')
        try:
            renderEntity['id'] = int(renderEntity['id'])
        except Exception ,err :
            print "[ERROR] set renderEntity['id'] , %s [ERROR]"  % err
        return renderEntity
    

