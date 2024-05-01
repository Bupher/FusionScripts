import adsk, adsk.core, adsk.fusion, adsk.cam, traceback

app = adsk.core.Application.get()
ui = app.userInterface

WORKSPACE_ID = 'FusionSolidEnvironment'
TOOLBARTAB_ID = "ToolsTab"
TOOLBARPANEL_ID = "SolidScriptsAddinsPanel"
CMD_ID = "ExtrudeJoin"

_handlers = []

def run(context):
    global _handlers

    cmdDef = ui.commandDefinitions.itemById(CMD_ID)
    if not cmdDef:
        cmdDef = ui.commandDefinitions.addButtonDefinition(CMD_ID, CMD_ID, CMD_ID, ".\\")
    onCommandCreated = scriptExecuteHandler()
    cmdDef.commandCreated.add(onCommandCreated)
    _handlers.append(onCommandCreated)

    workspace = ui.workspaces.itemById(WORKSPACE_ID)
    toolbar_tab = workspace.toolbarTabs.itemById(TOOLBARTAB_ID)
    panel = toolbar_tab.toolbarPanels.itemById(TOOLBARPANEL_ID)
    control = panel.controls.addCommand(cmdDef)
    control.isPromoted = True


def stop(context):
    global _handlers
    _handlers = []

    try:
        ui.commandDefinitions.itemById(CMD_ID).deleteMe()
    except:
        pass

    workspace = ui.workspaces.itemById(WORKSPACE_ID)
    toolbar_tab = workspace.toolbarTabs.itemById(TOOLBARTAB_ID)
    panel = toolbar_tab.toolbarPanels.itemById(TOOLBARPANEL_ID)
    try:
        panel.controls.itemById(CMD_ID).deleteMe()
    except:
        pass

class scriptExecuteHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, eventArgs: adsk.core.CommandCreatedEventArgs) -> None:
        # TODO: your script goes here!!!
        app = adsk.core.Application.get()
        ui  = app.userInterface
        selections = ui.activeSelections
        
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        rootComp = design.rootComponent
        sketches = rootComp.sketches

        if selections.count==1:
            for selection in selections:
                selectedEnt = selection.entity
                if selectedEnt.objectType == adsk.fusion.Profile.classType():
                    selectedProfile = selectedEnt
                    #distance = adsk.core.ValueInput.createByString("-17 mm")
                    input_result = ui.inputBox("Enter a distance in millimeters:", "Distance Input")
                    if input_result[0]:  # Check if the user clicked OK
                        input_distance = float(input_result[0])/10
                        distance = adsk.core.ValueInput.createByReal(input_distance)
                        operation = adsk.fusion.FeatureOperations.JoinFeatureOperation
                        extrudeFeatures = rootComp.features.extrudeFeatures
                        extrudeFeature = extrudeFeatures.addSimple(selectedProfile, distance, operation)
                        selectedProfile.parentSketch.isVisible = True
                    else:
                        # Handle the case where the user clicked Cancel
                        ui.messageBox("Operation cancelled.")                    
        app.log(f'{eventArgs.firingEvent.sender.name} executed!')