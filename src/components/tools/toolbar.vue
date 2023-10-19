<template>
  <!--draggable tool bar-->
  <v-card
    class="d-flex flex-column flex-nowrap position-absolute bg-light user-select-none overflow-y-hidden not-selectable"
    style="z-index: 99; cursor: pointer; max-height: 90vh; max-width: 50vh"
    :class="[collapsed ? 'rounded-0  bg-grey-darken-2' : 'bg-light']">
    <v-card-title ref="draggableDiv" :style="{ width: titleWidth }" class="pa-1">
      <v-tooltip v-model="showRightClickTooltip" location="right">
        <template v-slot:activator="{ props }">
          <v-btn icon="mdi-drag-horizontal" variant="plain" v-bind="props" class="rounded-0"
            :class="[collapsed ? ' rounded-0 rounded-be-xl' : '']" @contextmenu="handleRightClick">
          </v-btn>
        </template>
        <span>Right Click to Collapse/Expand</span>
      </v-tooltip>
    </v-card-title>
    <v-fade-transition>
      <v-card-text class="overflow-y-auto pa-1" v-show="!collapsed">
        <v-expansion-panels variant="accordion">
          <!--windows-->
          <v-expansion-panel>
            <v-expansion-panel-title>
              Windows
              <v-tooltip v-model="showWindowTooltip" location="right">
                <template v-slot:activator="{ props }">
                  <v-btn icon="mdi-help-circle-outline" variant="plain" v-bind="props" class="rounded-0"
                    style="position: absolute; right: 10%;" :ripple="false">
                  </v-btn>
                </template>
                <span>Add or delete different windows in the right hand side.</span><br />
                <span>1. K Neighbor Window: Show K Neighbors graph of selected node.</span><br />
                <span>2. AutoTree Window: Show AutoTree graph.</span><br />
                <span>3. Metrics Report Window: Show a summary of detailed metrics currently analyzed.</span><br />
                <span>4. Degree Distribution Window: Show degree distribution of all nodes/SSM node pairs.</span><br />
                <span>5. Customized IM Window: Show a customized IM graph acting as a competitor to the left hand
                  side.</span><br />
              </v-tooltip>
            </v-expansion-panel-title>
            <v-expansion-panel-text>
              <v-container class="pa-0">
                <v-select :items="windowNameList" v-model="windowSelected" label="Select Window" hide-details
                  class="mb-2"></v-select>
                <v-row>
                  <v-col cols="12" sm="6" class="pr-1">
                    <v-select :items="[1, 2]" v-model="colWidthSelected" label="Column Width" hide-details></v-select>
                  </v-col>

                  <v-col cols="12" sm="6" class="pl-1">
                    <v-select :items="[1, 2]" v-model="rowHeightSelected" label="Row Height" hide-details></v-select>
                  </v-col>
                </v-row>
              </v-container>
              <v-row>
                <v-col class="pr-1">
                  <v-btn color="success" class="w-50" realCol="1" realRow="1" block
                    @click="addComponentEmit()">Add</v-btn></v-col>
                <v-col class="pl-1">
                  <v-btn color="red" class="w-50" realCol="1" realRow="1" block
                    @click="removeComponentEmit()">Delete</v-btn></v-col>
              </v-row>
              <v-snackbar v-model="hasWindowSnackbar">
                Window already added!

                <template v-slot:actions>
                  <v-btn color="pink" variant="text" @click="hasWindowSnackbar = false">
                    Close
                  </v-btn>
                </template>
              </v-snackbar>
              <v-snackbar v-model="noWindowSnackbar">
                Window does not exist!

                <template v-slot:actions>
                  <v-btn color="pink" variant="text" @click="noWindowSnackbar = false">
                    Close
                  </v-btn>
                </template>
              </v-snackbar>
            </v-expansion-panel-text>
          </v-expansion-panel>
          <!--basic-->
          <v-expansion-panel>
            <v-expansion-panel-title>Basic
              <v-tooltip v-model="showBasicTooltip" location="right">
                <template v-slot:activator="{ props }">
                  <v-btn icon="mdi-help-circle-outline" variant="plain" v-bind="props" class="rounded-0"
                    style="position: absolute; right: 10%;" :ripple="false">
                  </v-btn>
                </template>
                <span>View basic metrics of the current graph.</span>
              </v-tooltip></v-expansion-panel-title>
            <v-expansion-panel-text>
              <v-tooltip v-model="showOrigRenderBtnTooltip" location="right">
                <template v-slot:activator="{ props }">
                  <v-btn ref="origRenderBtn" color="primary" block v-bind="props" @click="renderOrigColormap"
                    append-icon="mdi-palette">Render Basic</v-btn>
                </template>
                <span>Render graph based on degree of nodes.</span>
              </v-tooltip>
              <v-table class="w-100 h-100 text-no-wrap" density="compact" hover>
                <thead>
                  <tr class="">
                    <th class="w-50">METRIC</th>
                    <th class="">VALUE</th>
                  </tr>
                </thead>
                <tbody class="">
                  <tr>
                    <td class="w-50">Nodes</td>
                    <td v-if="origFullGraphStore.hasAnalyzedOrig">
                      {{ origFullGraphStore.nodeNum }}
                    </td>
                  </tr>
                  <tr>
                    <td class="w-50">Edges</td>
                    <td v-if="origFullGraphStore.hasAnalyzedOrig">
                      {{ origFullGraphStore.edgeNum }}
                    </td>
                  </tr>
                  <tr>
                    <td class="w-50">Avg Degree</td>
                    <td v-if="origFullGraphStore.hasAnalyzedOrig">
                      {{
                        origFullGraphStore.avgDegree.toString().substring(0, 12)
                      }}
                    </td>
                  </tr>
                  <tr>
                    <td class="w-50">Max Degree</td>
                    <td v-if="origFullGraphStore.hasAnalyzedOrig">
                      {{ origFullGraphStore.maxDegree }}
                    </td>
                  </tr>
                  <tr>
                    <td class="w-50">Density</td>
                    <td v-if="origFullGraphStore.hasAnalyzedOrig">
                      {{ graphologyStore.density.toString().substring(0, 12) }}
                    </td>
                  </tr>
                </tbody>
              </v-table>
            </v-expansion-panel-text>
          </v-expansion-panel>
          <!--k neighbor-->
          <v-expansion-panel>
            <v-expansion-panel-title>K Neighbor
              <v-tooltip v-model="showKNeighborTooltip" location="right">
                <template v-slot:activator="{ props }">
                  <v-btn icon="mdi-help-circle-outline" variant="plain" v-bind="props" class="rounded-0"
                    style="position: absolute; right: 10%;" :ripple="false">
                  </v-btn>
                </template>
                <span>View K-Neighbor metrics based on the node selected in the left hand side.</span>
              </v-tooltip></v-expansion-panel-title>
            <v-expansion-panel-text>
              <v-text-field label="Input K Value" v-model="kNeighborStore.kValue" class="mt-2" hide-details>
                <template v-slot:append>
                  <v-icon icon="mdi-plus" color="green" @click="addKValue">
                  </v-icon>
                </template>
                <template v-slot:prepend>
                  <v-icon icon="mdi-minus" color="red" @click="minusKValue">
                  </v-icon>
                </template>
              </v-text-field>
              <v-table class="w-100 h-100 text-no-wrap" density="compact" hover>
                <thead>
                  <tr class="">
                    <th class="w-50">METRIC</th>
                    <th class="">VALUE</th>
                  </tr>
                </thead>
                <tbody class="">
                  <tr>
                    <td class="w-50">Node ID</td>
                    <td>
                      {{
                        origFullGraphStore.selectedNode === undefined
                        ? ""
                        : origFullGraphStore.selectedNode
                      }}
                    </td>
                  </tr>
                  <tr>
                    <td class="w-50">K-Neighbor Num</td>
                    <td>
                      {{
                        kNeighborStore.kNeighborNum === 0
                        ? ""
                        : kNeighborStore.kNeighborNum - 1
                      }}
                    </td>
                  </tr>
                  <tr>
                    <td class="w-50">Degree</td>
                    <td>
                      {{
                        Object.keys(origFullGraphStore.selectedNodeStats)
                          .length === 0
                        ? ""
                        : origFullGraphStore.selectedNodeStats.degree.toString()
                      }}
                    </td>
                  </tr>
                  <tr>
                    <td class="w-50">Degree Centrality</td>
                    <td>
                      {{
                        Object.keys(origFullGraphStore.selectedNodeStats)
                          .length === 0
                        ? ""
                        : origFullGraphStore.selectedNodeStats.degreeCentrality
                          .toString()
                          .substring(0, 12)
                      }}
                    </td>
                  </tr>
                  <tr>
                    <td class="w-50">Pagerank</td>
                    <td>
                      {{
                        Object.keys(origFullGraphStore.selectedNodeStats)
                          .length === 0
                        ? ""
                        : origFullGraphStore.selectedNodeStats.pagerank
                          .toString()
                          .substring(0, 12)
                      }}
                    </td>
                  </tr>
                </tbody>
              </v-table>
              <v-snackbar v-model="kNeighborValueSnackbar">
                K value must be positive!

                <template v-slot:actions>
                  <v-btn color="pink" variant="text" @click="kNeighborValueSnackbar = false">
                    Close
                  </v-btn>
                </template>
              </v-snackbar>
            </v-expansion-panel-text>
          </v-expansion-panel>
          <!--autotree-->
          <v-expansion-panel :disabled="!autoTreeStore.hasReceivedAutoTree">
            <v-expansion-panel-title>AutoTree
              <v-tooltip v-model="showAutoTreeTooltip" location="right">
                <template v-slot:activator="{ props }">
                  <v-btn icon="mdi-help-circle-outline" variant="plain" v-bind="props" class="rounded-0"
                    style="position: absolute; right: 10%;" :ripple="false">
                  </v-btn>
                </template>
                <span>AutoTree helps to locate SSM pairs in the whole graph.</span>
              </v-tooltip></v-expansion-panel-title>
            <v-expansion-panel-text>
              <v-tooltip v-model="showATRenderBtnTooltip" location="right">
                <template v-slot:activator="{ props }">
                  <v-btn ref="atRenderBtn" color="secondary" block v-bind="props" @click="createATGraph"
                    append-icon="mdi-graph-outline">Generate AutoTree</v-btn>
                </template>
                <span>Render AutoTree in the added window.</span>
              </v-tooltip>
              <v-divider v-show="autoTreeCreated" :thickness="2" class="mt-2 mb-2" color="white"></v-divider>
              <v-scroll-x-transition>
                <v-tooltip v-model="showATDestoryBtnTooltip" location="right">
                  <template v-slot:activator="{ props }">
                    <v-btn ref="atDestroyBtn" :color="asteroidDestroyed ? 'grey-darken-3' : 'warning'" block
                      @click="asteroidDestroy" append-icon="mdi-delete" v-show="autoTreeCreated"
                      :disabled="asteroidDestroyed" v-bind="props">Destroy Asteroid</v-btn>
                  </template>
                  <span>Delete useless leaf nodes in the AutoTree.</span>
                </v-tooltip>
              </v-scroll-x-transition>
              <v-snackbar v-model="autoTreeSnackbar">
                AutoTree window has not been initialized!

                <template v-slot:actions>
                  <v-btn color="pink" variant="text" @click="autoTreeSnackbar = false">
                    Close
                  </v-btn>
                </template>
              </v-snackbar>
            </v-expansion-panel-text>
          </v-expansion-panel>
          <!--ssm-->
          <v-expansion-panel :disabled="!origFullGraphStore.hasReceivedSSM">
            <v-expansion-panel-title>SSM
              <v-tooltip v-model="showSSMTooltip" location="right">
                <template v-slot:activator="{ props }">
                  <v-btn icon="mdi-help-circle-outline" variant="plain" v-bind="props" class="rounded-0"
                    style="position: absolute; right: 10%;" :ripple="false">
                  </v-btn>
                </template>
                <span>Symmetric Subgraph Matching helps to detect automorphism subgraphs.</span>
              </v-tooltip></v-expansion-panel-title>
            <v-expansion-panel-text><v-tooltip v-model="showSSMRenderBtnTooltip" location="right">
                <template v-slot:activator="{ props }">
                  <v-btn ref="ssmRenderBtn" realCol="1" realRow="1" color="primary" block @click="renderSSMColormap"
                    append-icon="mdi-palette" v-bind="props">Render SSM</v-btn>
                </template>
                <span>Render graph based on SSM (non-SSM pairs will be greyed out).</span>
              </v-tooltip>

              <v-table class="w-100 h-100 text-no-wrap" density="compact" hover>
                <thead>
                  <tr class="">
                    <th class="w-50">METRIC</th>
                    <th class="">VALUE</th>
                  </tr>
                </thead>
                <tbody class="">
                  <!--ssm stats-->
                  <tr>
                    <td class="w-50">Non-Singular Count</td>
                    <td>
                      {{
                        origFullGraphStore.ssmNonSingularCount === 0
                        ? ""
                        : origFullGraphStore.ssmNonSingularCount
                      }}
                    </td>
                  </tr>
                  <tr>
                    <td class="w-50">Avg Degree</td>
                    <td>
                      {{
                        origFullGraphStore.ssmAvgDegree === 0
                        ? ""
                        : origFullGraphStore.ssmAvgDegree
                          .toFixed(12)
                          .toString()
                          .substring(0, 6)
                      }}
                    </td>
                  </tr>
                  <tr>
                    <td class="w-50">Max Degree</td>
                    <td>
                      {{
                        origFullGraphStore.ssmMaxDegree === 0
                        ? ""
                        : origFullGraphStore.ssmMaxDegree
                      }}
                    </td>
                  </tr>
                </tbody>
              </v-table>
            </v-expansion-panel-text>
          </v-expansion-panel>
          <!--im-->
          <v-expansion-panel><!--:disabled="!origFullGraphStore.hasReceivedIM"-->
            <v-expansion-panel-title>IM
              <v-tooltip v-model="showIMTooltip" location="right">
                <template v-slot:activator="{ props }">
                  <v-btn icon="mdi-help-circle-outline" variant="plain" v-bind="props" class="rounded-0"
                    style="position: absolute; right: 10%;" :ripple="false">
                  </v-btn>
                </template>
                <span>1. Get pruned/unpruned seed set from 'Integrated Methods';</span><br />
                <span>2. Submit request/Render graph with the chosen seed set in 'Customized Rendering';</span><br />
                <span>3. View detailed metrics and visualize stepwise in 'Stepwise Visualization'.</span>
              </v-tooltip></v-expansion-panel-title>
            <v-expansion-panel-text>
              <v-expansion-panels variant="accordion">
                <v-tooltip v-model="showIMRenderBtnTooltip" location="right">
                  <template v-slot:activator="{ props }">
                    <v-btn ref="imRenderBtn" color="primary" block v-bind="props" @click="renderIMColormap"
                      append-icon="mdi-palette">Render
                      IM</v-btn>
                  </template>
                  <span>Render influence spread in the left hand side if a render request has been submitted before in
                    'Customized Rendering'.</span>
                </v-tooltip>
                <v-expansion-panel elevation="19">
                  <v-expansion-panel-title>
                    Integrated Methods
                    <v-tooltip v-model="showIntegratedMethodsTooltip" location="right">
                      <template v-slot:activator="{ props }">
                        <v-btn icon="mdi-help-circle-outline" variant="plain" v-bind="props" class="rounded-0"
                          style="position: absolute; right: 10%;" :ripple="false">
                        </v-btn>
                      </template>
                      <span>Use integrated IM methods to select seeds for influence spread.</span>
                    </v-tooltip>
                  </v-expansion-panel-title>
                  <v-expansion-panel-text>
                    <v-card class="text-center w-100 pt-2 pb-2 ps-0 pe-0 mb-2" elevation="0">
                      <v-dialog v-model="uploadMethodDialog" width="30rem">
                        <template v-slot:activator="{ props }">
                          <v-btn color="primary" class="w-100" variant="tonal" v-bind="props">
                            Upload New Method
                          </v-btn>
                        </template>

                        <v-card>
                          <v-card-item>
                            <v-card-title class="text-overline">
                              Upload your own method
                            </v-card-title>
                          </v-card-item>
                          <v-card-text>
                            <v-file-input label="Input file(s)" multiple chips></v-file-input>
                            <v-form @submit.prevent="newMethodSubmit">
                              <v-text-field label="Name your method" hide-details
                                v-model="uploadMethodName"></v-text-field>
                              <p class="text-caption">
                                Your dir is: ./flask/methods/userMethods/{{
                                  uploadMethodName == ""
                                  ? "?"
                                  : uploadMethodName
                                }}
                              </p>
                              <p class="text-caption">
                                Path of graph file is: ./flask/usrfile.txt
                              </p>
                              <v-textarea label="Enter your commands to run the method"
                                v-model="uploadMethodCommand"></v-textarea>
                            </v-form>
                          </v-card-text>
                          <v-card-actions>
                            <v-btn color="primary" class="w-50" @click="newMethodSubmit">Submit</v-btn>
                            <v-btn color="primary" class="w-50 ms-0" @click="uploadMethodDialog = false">Close
                              Dialog</v-btn>
                          </v-card-actions>
                        </v-card>
                      </v-dialog>
                    </v-card>
                    <v-form @submit.prevent="methodSubmit">
                      <v-select label="Select Method" :items="methodTypeList" v-model="methodType" variant="outlined"
                        hide-details></v-select><!--
                      <v-switch inset label="DIY Parameters" v-model="isDIYParameters" hide-details></v-switch>
                      <template v-if="isDIYParameters">
                        <v-text-field clearable label="Input your own parameters..." v-model="diyParameters"></v-text-field>
                      </template>
                      <template v-else>-->
                      <v-text-field append-icon="mdi-counter" label="Seed Size" v-model="methodSeedSize" type="number"
                        hide-details></v-text-field>
                      <v-text-field append-icon="mdi-map-marker-path" label="Decay" v-show="methodType == 'PMC'"
                        v-model="pmcDecay" hide-details type="number"></v-text-field>
                      <v-text-field append-icon="mdi-percent-outline" v-show="methodType == 'PMC'"
                        label="Spread Probability (%)" v-model="spreadProbability" type="number"></v-text-field>
                      <v-text-field v-show="methodType == 'SSA' || methodType == 'DSSA'" label="Epsilon"
                        v-model="ssaEpsilon" hide-details type="number"></v-text-field>
                      <v-text-field v-show="methodType == 'SSA' || methodType == 'DSSA'" label="Delta" v-model="ssaDelta"
                        hide-details type="number"></v-text-field>
                      <v-select v-show="methodType == 'Subsim'" label="Probability Distribution" hide-details
                        :items="subsimPdistList" v-model="subsimPdist"></v-select>
                      <v-text-field v-show="methodType == 'Subsim' && subsimPdist == 'wc'" label="WC Variant"
                        v-model="subsimWCVariant" hide-details type="number"></v-text-field>
                      <v-text-field v-show="methodType == 'Subsim' && subsimPdist == 'uniform'
                        " label="Pedge" v-model="subsimPedge" hide-details type="number"></v-text-field>
                      <v-select v-show="methodType == 'Subsim' && subsimPdist == 'skewed'
                        " :items="['exp', 'weibull']" label="Skewed Distribution" v-model="subsimSkewedDist"
                        hide-details></v-select>
                      <v-text-field v-show="methodType == 'Subsim'" label="Epsilon" v-model="subsimEps" hide-details
                        type="number"></v-text-field>
                      <v-text-field v-show="methodType == 'Subsim'" label="Delta" v-model="subsimDelta" hide-details
                        type="number"></v-text-field>
                      <v-select v-show="methodType == 'Subsim'" label="RR Set Generation Method"
                        :items="['Subsim', 'Vanilla']" v-model="subsimVanilla" hide-details></v-select>
                      <v-select v-show="methodType == 'Subsim'" label="Invoke HIST Algorithm" :items="['False', 'True']"
                        v-model="subsimHist"></v-select>
                      <v-select v-show="methodType == 'SSA' || methodType == 'DSSA'" label="Diffusion Model"
                        :items="ssaModelList" v-model="ssaModel"></v-select>

                      <v-tooltip v-model="showIntegratedMethodsSubmitTooltip" location="right">
                        <template v-slot:activator="{ props }">
                          <v-btn type="submit" v-bind="props" block class="mt-2" append-icon="mdi-send">Submit</v-btn>
                        </template>
                        <span>Once the result is returned, you can directly jump to 'Customized Rendering' to submit
                          render request if pruning is not used.</span>
                      </v-tooltip><!--
                      <v-table
                        class="w-100 h-100 text-no-wrap"
                        density="compact"
                        hover
                      >
                        <thead>
                          <tr class="">
                            <th class="w-50">METRIC</th>
                            <th class="">VALUE</th>
                          </tr>
                        </thead>
                        <tbody class="">
                          <tr>
                            <td class="w-50">Metric 1</td>
                            <td>{{}}</td>
                          </tr>
                          <tr>
                            <td class="w-50">Metric 2</td>
                            <td>{{}}</td>
                          </tr>
                          <tr>
                            <td class="w-50">Metric 3</td>
                            <td>{{}}</td>
                          </tr>
                        </tbody>
                      </v-table>-->
                      <v-divider></v-divider>
                      <v-combobox v-model="selectedNodesFromMethod" multiple chips label="Unpruned Result"
                        hide-details></v-combobox>
                      <v-divider></v-divider>
                      <v-tooltip v-model="showHighlightCustomizedNodesFromMethodTooltip" location="right">
                        <template v-slot:activator="{ props }">
                          <v-btn block class="mt-2 bg-info" append-icon="mdi-magnify-expand" v-bind="props"
                            @click="highlightCustomizedNodesFromMethod">Highlight</v-btn>
                        </template>
                        <span>Highlight the chosen nodes in the left hand side.</span>
                      </v-tooltip>
                      <v-tooltip v-model="showPruneBtnTooltip" location="right">
                        <template v-slot:activator="{ props }">
                          <v-btn block class="mt-2 bg-amber" append-icon="mdi-content-cut" @click="ipSubmit"
                            v-bind="props">Prune</v-btn>
                        </template>
                        <span>NOTE: Pruning is *very* time-consuming!</span><br/>
                        <span>Prune the current seed set using our proposed pruning method;</span><br />
                        <span>If you want to use the pruned result, Click 'Retrieve Data' to copy it to 'Customized
                          Rendering'.</span>
                      </v-tooltip>
                      <!--
                      <v-table
                        class="w-100 h-100 text-no-wrap"
                        density="compact"
                        hover
                        hide-details
                      >
                        <thead>
                          <tr class="">
                            <th class="w-50">METRIC</th>
                            <th class="">VALUE</th>
                          </tr>
                        </thead>
                        <tbody class="">
                          <tr>
                            <td class="w-50">Metric 1</td>
                            <td>{{}}</td>
                          </tr>
                          <tr>
                            <td class="w-50">Metric 2</td>
                            <td>{{}}</td>
                          </tr>
                          <tr>
                            <td class="w-50">Metric 3</td>
                            <td>{{}}</td>
                          </tr>
                        </tbody>
                      </v-table>-->
                      <v-divider></v-divider>
                      <v-combobox v-model="selectedNodesFromIP" multiple chips label="Pruned Result"
                        hide-details></v-combobox>
                      <v-combobox v-model="prunedNodesFromIP" multiple chips label="Replaced Nodes"
                        hide-details></v-combobox>
                      <v-combobox v-model="newNodesFromIP" multiple chips label="Introduced Nodes"
                        hide-details></v-combobox>

                      <v-divider></v-divider>
                      <v-tooltip v-model="showHighlightCustomizedNodesFromIPTooltip" location="right">
                        <template v-slot:activator="{ props }">
                          <v-btn block class="mt-2 bg-info" append-icon="mdi-magnify-expand"
                            @click="highlightCustomizedNodesFromIP" v-bind="props">Highlight</v-btn>
                        </template>
                        <span>Highlight the pruned seed set in the left hand side.</span>
                      </v-tooltip>
                      <v-tooltip v-model="showTransferIPResultToRenderTooltip" location="right">
                        <template v-slot:activator="{ props }">
                          <v-btn block class="mt-2 bg-success" append-icon="mdi-send" v-bind="props"
                            @click="transferIPResultToRender">Retrieve Data</v-btn>
                        </template>
                        <span>Copy pruned data to 'Customized Rendering'.</span>
                      </v-tooltip>
                    </v-form>

                    <v-snackbar v-model="hasRetrievedDataSnackbar">
                      Retrieve successfully. Please check the input box in
                      "Customized Rendering"!

                      <template v-slot:actions>
                        <v-btn color="pink" variant="text" @click="methodSeedHasReturnedSnackbar = false">
                          Close
                        </v-btn>
                      </template>
                    </v-snackbar>
                    <v-snackbar v-model="methodSeedHasReturnedSnackbar">
                      Result has returned successfully. Please check the input
                      box in "Customized Rendering"!

                      <template v-slot:actions>
                        <v-btn color="pink" variant="text" @click="methodSeedHasReturnedSnackbar = false">
                          Close
                        </v-btn>
                      </template>
                    </v-snackbar>
                    <v-snackbar v-model="methodSeedFailedToReturnSnackbar">
                      Result failed to return. Please check error log!

                      <template v-slot:actions>
                        <v-btn color="pink" variant="text" @click="methodSeedFailedToReturnSnackbar = false">
                          Close
                        </v-btn>
                      </template>
                    </v-snackbar>
                    <v-snackbar v-model="methodInputInvalidSnackbar">
                      Invalid input! Please check again.

                      <template v-slot:actions>
                        <v-btn color="pink" variant="text" @click="methodInputInvalidSnackbar = false">
                          Close
                        </v-btn>
                      </template>
                    </v-snackbar>

                    <v-snackbar v-model="selectedNodesFromIPFallbackSnackbar">
                      Invalid Input for IP!

                      <template v-slot:actions>
                        <v-btn color="pink" variant="text" @click="selectedNodesForIMFallbackSnackbar = false">
                          Close
                        </v-btn>
                      </template>
                    </v-snackbar>
                    <v-snackbar v-model="ipSeedHasReturnedSnackbar">
                      IP result has returned successfully.

                      <template v-slot:actions>
                        <v-btn color="pink" variant="text" @click="ipSeedHasReturnedSnackbar = false">
                          Close
                        </v-btn>
                      </template>
                    </v-snackbar>
                    <v-snackbar v-model="ipSeedFailedToReturnSnackbar">
                      IP result failed to return. Please check error log!

                      <template v-slot:actions>
                        <v-btn color="pink" variant="text" @click="ipSeedFailedToReturnSnackbar = false">
                          Close
                        </v-btn>
                      </template>
                    </v-snackbar>
                  </v-expansion-panel-text>
                </v-expansion-panel>
                <v-expansion-panel elevation="19">
                  <v-expansion-panel-title>
                    Customized Rendering
                    <v-tooltip v-model="showCustomizedRenderingTooltip" location="right">
                      <template v-slot:activator="{ props }">
                        <v-btn icon="mdi-help-circle-outline" variant="plain" v-bind="props" class="rounded-0"
                          style="position: absolute; right: 10%;" :ripple="false">
                        </v-btn>
                      </template>
                      <span>1. Choose nodes as influence spread seed set. You can add nodes by: </span><br />
                      <span>Clicking nodes in the left hand side/Type in node ID manually/Retrieve from 'Integrated
                        Methods';</span><br /><br />
                      <span>2. Configure spread model and corresponding params;</span><br /><br />
                      <span>3. Before submission, enable/disable "Use Customized IM Container": <br /> Enabling will render the
                        graph in 'Customized IM window', else will render directly in the left hand
                        side;</span><br /><br />
                      <span>4. Submit, and render graph after result is retrieved.</span>

                    </v-tooltip>
                  </v-expansion-panel-title>
                  <v-expansion-panel-text>
                    <v-form @submit.prevent="customizedIMSubmit">
                      <v-combobox v-model="selectedNodesForIM" multiple chips clearable
                        label="Choose Nodes (input twice for deletion)" hide-details></v-combobox>
                      <v-select :items="['IC', 'LT']" v-model="spreadModel" label="Spread Model" hide-details>

                      </v-select>
                      <v-text-field append-icon="mdi-percent-outline" label="Spread Probability (%)"
                        v-if="spreadModel == 'IC'" v-model="spreadProbability" type="number"></v-text-field>
                      <v-text-field label="Time Limit (Number of Rounds)" v-else v-model="timeLimit" type="number">

                      </v-text-field>
                      <v-tooltip v-model="showHighlightCustomizedNodesTooltip" location="right">
                        <template v-slot:activator="{ props }">
                          <v-btn block class="mt-2 bg-info" append-icon="mdi-magnify-expand" v-bind="props"
                            @click="highlightCustomizedNodes">Highlight</v-btn>
                        </template>
                        <span>Hightlight selected nodes in the left hand side.</span>

                      </v-tooltip>
                      <v-checkbox label="Use Customized IM Container" v-model="customizedIMStore.useNewContainer"
                        hide-details></v-checkbox>

                      <v-tooltip v-model="showCustomizedIMRenderSubmitBtnTooltip" location="right">
                        <template v-slot:activator="{ props }">
                          <v-btn type="submit" block class="mb-2" append-icon="mdi-send" v-bind="props">Submit</v-btn>
                        </template>
                        <span>Submit seed set & spread settings to the backend.</span>

                      </v-tooltip>
                      <v-tooltip v-model="showCustomizedIMRenderBtnTooltip" location="right">
                        <template v-slot:activator="{ props }">
                          <v-btn ref="customizedIMRenderBtn" color="success" block @click="renderCustomizedIMColormap"
                            :loading="!customizedIMStore.hasReceived" :disabled="!customizedIMStore.hasReceived"
                            v-bind="props" append-icon="mdi-palette">Customized Render</v-btn>
                        </template>
                        <span>Render influence spread in the chosen container.</span>

                      </v-tooltip>
                    </v-form>
                    <v-row><v-col sm="6" class="pr-1"> </v-col><v-col sm="6" class="pl-1"></v-col></v-row>
                    <v-snackbar v-model="selectedNodesForIMFallbackSnackbar">
                      Invalid Input for Customized IM!

                      <template v-slot:actions>
                        <v-btn color="pink" variant="text" @click="selectedNodesForIMFallbackSnackbar = false">
                          Close
                        </v-btn>
                      </template>
                    </v-snackbar>
                    <v-snackbar v-model="customizedIMSnackbar">
                      Customized IM window has not been initialized!

                      <template v-slot:actions>
                        <v-btn color="pink" variant="text" @click="customizedIMSnackbar = false">
                          Close
                        </v-btn>
                      </template>
                    </v-snackbar>
                  </v-expansion-panel-text>
                </v-expansion-panel>
                <v-expansion-panel elevation="19">
                  <v-expansion-panel-title>
                    Stepwise Visualization
                    <v-tooltip v-model="showStepwiseVisualizationTooltip" location="right">
                      <template v-slot:activator="{ props }">
                        <v-btn icon="mdi-help-circle-outline" variant="plain" v-bind="props" class="rounded-0"
                          style="position: absolute; right: 10%;" :ripple="false">
                        </v-btn>
                      </template>
                      <span>View stepwise metrics and corresponding nodes;<br /> Use toggle to hide/unhide nodes in the
                        specific round;<br />Select 'Stepwise View' to enable/disable toggles view effects in left/right
                        container.</span>
                    </v-tooltip>
                  </v-expansion-panel-title>
                  <v-expansion-panel-text>
                    <v-col class="d-flex flex-column justify-center pa-0">
                      <v-tooltip v-model="showRandomColorTooltip" location="right">
                        <template v-slot:activator="{ props }">
                          <v-btn block class="pa-0" color="primary" append-icon="mdi-palette-swatch-variant"
                            v-bind="props" @click="randomColorGenerator()">Random Color</v-btn>
                        </template>
                        <span>Assign random color to different rounds. You can preview the color combination by toggles
                          until satisfied, then click 'Render IM'/'Customized Render'.</span>
                      </v-tooltip>

                      <v-row class="w-100 d-flex flex-row pa-0 ma-0 justify-start align-start">
                        <v-col col="12" sm="4" class="ps-0 pe-0 text-subtitle-2">Algorithm</v-col>
                        <v-col col="12" sm="4" class="ps-0 pe-0 text-center" style="white-space: pre-wrap">
                          {{ leftMethodName }}
                        </v-col>
                        <v-col col="12" sm="4" class="ps-0 pe-0 text-center" style="white-space: pre-wrap">
                          {{ rightMethodName }}
                        </v-col>
                      </v-row>

                      <v-row class="w-100 d-flex flex-row pa-0 ma-0 justify-start align-start">
                        <v-col col="12" sm="4" class="ps-0 pe-0 text-subtitle-2">Params</v-col>
                        <v-col col="12" sm="4" class="ps-0 pe-0 justify-center d-flex">
                          <v-btn variant="text" density="compact"
                            class="text-body-2 text-decoration-underline font-weight-regular">
                            View Here
                            <v-tooltip activator="parent" location="bottom" style="white-space: pre-wrap">{{
                              leftMethodParameters }}</v-tooltip>
                          </v-btn>
                        </v-col>
                        <v-col col="12" sm="4" class="ps-0 pe-0 justify-center d-flex">
                          <v-btn variant="text" density="compact"
                            class="text-body-2 text-decoration-underline font-weight-regular">
                            View Here
                            <v-tooltip activator="parent" location="bottom" style="white-space: pre-wrap">{{
                              rightMethodParameters }}</v-tooltip>
                          </v-btn>
                        </v-col>
                      </v-row>

                      <v-row class="w-100 d-flex flex-row pa-0 ma-0 justify-start align-start">
                        <v-col col="12" sm="4" class="ps-0 pe-0 text-subtitle-2">Seed Metrics</v-col>
                        <v-col col="12" sm="8" class="ps-0 pe-0 justify-center d-flex">
                          <v-dialog v-model="seedSetComparisonDialog" width="50rem">
                            <template v-slot:activator="{ props }">
                              <v-btn variant="text" density="compact"
                                class="text-body-2 text-decoration-underline font-weight-regular" v-bind="props">
                                Click Here
                                <v-tooltip activator="parent" location="bottom" style="white-space: pre-wrap">{{
                                  leftMethodParameters }}</v-tooltip>
                              </v-btn>
                            </template>

                            <v-card>
                              <v-card-item>
                                <v-card-title class="text-overline">
                                  Seed Set Metrics
                                </v-card-title>
                              </v-card-item>
                              <v-card-text>
                                <p class="text-overline">Distribution Comparison</p>
                                <v-select v-model="binaryComparisonOption"
                                  :items="Object.keys(binaryComparisonOptionList)"></v-select>
                                <Chart :options="binaryComparisonOptionList[binaryComparisonOption]"></Chart>
                                <p class="text-overline">Sum Comparison</p>
                                <Chart :options="summationComparisonOption"></Chart>
                              </v-card-text>
                              <v-card-actions>
                                <v-btn color="primary" class="" @click="seedSetComparisonDialog = false">Close
                                  Dialog</v-btn>
                              </v-card-actions>
                            </v-card>
                          </v-dialog>
                        </v-col>
                      </v-row>

                      <v-row class="w-100 d-flex flex-row pa-0 ma-0 justify-start align-start">
                        <v-col col="12" sm="4" class="ps-0 pe-0 text-subtitle-2">Stepwise View</v-col>
                        <v-col col="12" sm="4" class="ps-0 pe-0">
                          <v-checkbox v-model="selectedIMGraph" value="Original" density="compact" class="center-checkbox"
                            hide-details></v-checkbox>
                        </v-col>
                        <v-col col="12" sm="4" class="ps-0 pe-0">
                          <v-checkbox v-model="selectedIMGraph" value="Competitor" density="compact"
                            class="center-checkbox" hide-details></v-checkbox>
                        </v-col>
                      </v-row>

                      <v-row class="w-100 d-flex flex-row justify-space-between pa-0 ma-0">
                        
                          <v-btn :disabled="currentVisibleIMStep <= -1" @click="decrementVisibleIMStep" color="primary">
                            <v-icon icon="mdi-chevron-left"></v-icon>
                            Last Step
                          </v-btn>

                          <v-btn :disabled="currentVisibleIMStep >= MaxRound" @click="incrementVisibleIMStep"  color="primary">
                            Next Step
                            <v-icon icon="mdi-chevron-right"></v-icon>
                          </v-btn>

                        
                      </v-row>
                      <v-col class="ps-0 pe-0">
                        <v-row class="w-100 ma-0">
                          <v-tooltip v-model="showClearShowRoundsTooltip" location="right">
                            <template v-slot:activator="{ props }">
                              <v-btn @click="clearShowRounds" color="red" block v-bind="props">
                                Clear Selections
                              </v-btn>
                            </template>
                            <span>Reset all toggles to false and unhide all nodes.</span>
                          </v-tooltip>
                        </v-row>
                        <!--position LHS/RHS-->
                        <v-row class="w-100 ma-0">
                          <v-divider></v-divider>
                          <v-col col="12" sm="6" class="pa-0 text-overline">
                            <span>Position</span>
                          </v-col>
                          <v-col col="12" sm="4"
                            class="pa-0 text-center d-flex justify-center align-center text-overline"><span>{{ "LHS"
                            }}</span></v-col>
                          <v-col col="12" sm="2" class="pa-0 text-center d-flex justify-center align-center text-overline"
                            v-if="customizedIMStore.imDistributionDict !== null">
                            <span>{{ "RHS" }}</span>
                          </v-col>
                        </v-row>
                        <v-row v-for="(color, round) in currentimRoundColorDict" :key="round" :style="{ color: color }"
                          class="w-100 ma-0">
                          <v-divider></v-divider>
                          <v-col col="12" sm="6" class="pa-0"><v-switch v-model="showRounds[round]"
                              :label="'Round ' + round" :color="color" hide-details inset
                              @change="showRoundHandler(round)"></v-switch></v-col>
                          <v-col col="12" sm="4" class="pa-0 text-center d-flex justify-center align-center text-body-1"
                            style="white-space: break-spaces" v-if="Object.keys(origFullGraphStore.imDistributionDict)
                              .length !== 0
                              "><span>{{
    Object.prototype.hasOwnProperty.call(
      origFullGraphStore.imDistributionDict,
      round
    )
    ? origFullGraphStore.imDistributionDict[round] +
    "\n(" +
    origFullGraphStore.imPercentDict[round]
      .toString()
      .substring(0, 4) +
    "%)"
    : ""
  }}</span></v-col>
                          <v-col col="12" sm="2" class="pa-0 text-center d-flex justify-center align-center text-body-1"
                            style="white-space: break-spaces" v-if="Object.keys(customizedIMStore.imDistributionDict)
                                  .length !== 0
                                ">
                            <span>{{
                              Object.prototype.hasOwnProperty.call(
                                customizedIMStore.imDistributionDict,
                                round
                              )
                              ? customizedIMStore.imDistributionDict[round] +
                              "\n(" +
                              customizedIMStore.imPercentDict[round]
                                .toString()
                                .substring(0, 4) +
                              "%)"
                              : ""
                            }}</span>
                          </v-col>
                        </v-row>
                        <v-row class="w-100 ma-0">
                          <v-divider></v-divider>
                          <v-col col="12" sm="6" class="pa-2 text-subtitle-1">
                            SUM
                          </v-col>
                          <v-col col="12" sm="4"
                            class="pa-0 text-center d-flex justify-center align-center text-body-1"><span>{{
                              Object.values(
                                origFullGraphStore.imDistributionDict
                              ).reduce((a, b) => a + b, 0)
                            }}</span></v-col>
                          <v-col col="12" sm="2"
                            class="pa-0 text-center d-flex justify-center align-center text-body-1"><span>{{
                              Object.keys(customizedIMStore.imDistributionDict)
                                .length == 0
                              ? ""
                              : Object.values(
                                customizedIMStore.imDistributionDict
                              ).reduce((a, b) => a + b, 0)
                            }}</span></v-col>
                        </v-row>
                        <v-row class="w-100 ma-0">
                          <v-divider></v-divider>
                          <v-col col="12" sm="6" class="pa-2 text-subtitle-1">
                            EFFICIENCY
                          </v-col>
                          <v-col col="12" sm="4"
                            class="pa-0 text-center d-flex justify-center align-center text-body-1"><span>{{
                              (
                                Object.values(
                                  origFullGraphStore.imDistributionDict
                                ).reduce((a, b) => a + b, 0) /
                                Object.keys(
                                  origFullGraphStore.imDistributionDict
                                ).length
                              )
                                .toString()
                                .substring(0, 5)
                            }}</span></v-col>
                          <v-col col="12" sm="2"
                            class="pa-0 text-center d-flex justify-center align-center text-body-1"><span>{{
                              Object.keys(customizedIMStore.imDistributionDict)
                                .length == 0
                              ? ""
                              : (
                                Object.values(
                                  customizedIMStore.imDistributionDict
                                ).reduce((a, b) => a + b, 0) /
                                Object.keys(
                                  customizedIMStore.imDistributionDict
                                ).length
                              )
                                .toString()
                                .substring(0, 5)
                            }}</span></v-col>
                        </v-row>
                        <v-row class="w-100 ma-0">
                          <v-divider></v-divider>
                          <v-col col="12" sm="6" class="pa-2 text-subtitle-1">
                            COVERAGE
                          </v-col>
                          <v-col col="12" sm="4"
                            class="pa-0 text-center d-flex justify-center align-center text-body-1"><span>{{
                              formatPercentage(
                                Object.values(
                                  origFullGraphStore.imDistributionDict
                                ).reduce((a, b) => a + b, 0) /
                                origFullGraphStore.nodeNum
                              )
                            }}</span></v-col>
                          <v-col col="12" sm="2"
                            class="pa-0 text-center d-flex justify-center align-center text-body-1"><span>{{
                              Object.keys(customizedIMStore.imDistributionDict)
                                .length == 0
                              ? ""
                              : formatPercentage(
                                Object.values(
                                  customizedIMStore.imDistributionDict
                                ).reduce((a, b) => a + b, 0) /
                                origFullGraphStore.nodeNum
                              )
                            }}</span></v-col>
                        </v-row>
                      </v-col>
                    </v-col>
                  </v-expansion-panel-text>
                </v-expansion-panel>
              </v-expansion-panels>
            </v-expansion-panel-text>
          </v-expansion-panel>
          <v-expansion-panel>
            <v-expansion-panel-title>Layout
              <v-tooltip v-model="showLayoutTooltip" location="right">
                <template v-slot:activator="{ props }">
                  <v-btn icon="mdi-help-circle-outline" variant="plain" v-bind="props" class="rounded-0"
                    style="position: absolute; right: 10%;" :ripple="false">
                  </v-btn>
                </template>
                <span>1. Change chosen graph's layout in real time.</span>

              </v-tooltip></v-expansion-panel-title>
            <v-expansion-panel-text>
              <v-select :items="configItems" v-model="configType" label="Select Config Type"
                prepend-icon="mdi-format-list-bulleted-type"></v-select>
              <div class="text-caption">Repulsion</div>
              <v-slider min="0" max="2" step="0.05" v-model="interfaceConfig.simulation.repulsion" thumb-label></v-slider>

              <div class="text-caption">Repulsion Theta</div>
              <v-slider min="0.3" max="2" step="0.05" v-model="interfaceConfig.simulation.repulsionTheta"
                thumb-label></v-slider>
              <!--
                <div class="text-caption">Repulsion Quadtree Levels</div>
                <v-slider min="5" max="12" step="1" v-model="origFullGraphConfig.simulation.repulsionQuadtreeLevels" thumb-label></v-slider>
                -->
              <div class="text-caption">Link Spring</div>
              <v-slider min="0" max="2" step="0.05" v-model="interfaceConfig.simulation.linkSpring"
                thumb-label></v-slider>

              <div class="text-caption">Link Distance</div>
              <v-slider min="1" max="20" step="0.5" v-model="interfaceConfig.simulation.linkDistance"
                thumb-label></v-slider>

              <div class="text-caption">
                Link Distance Random Variation Range
              </div>
              <v-range-slider v-model="interfaceConfig.simulation.linkDistRandomVariationRange
                " min="0.8" max="2.0" step="0.05" thumb-label></v-range-slider>

              <div class="text-caption">Gravity</div>
              <v-slider min="0" max="1" step="0.01" v-model="interfaceConfig.simulation.gravity" thumb-label></v-slider>

              <div class="text-caption">Center</div>
              <v-slider min="0" max="1" step="0.01" v-model="interfaceConfig.simulation.center" thumb-label></v-slider>

              <div class="text-caption">Friction</div>
              <v-slider min="0.8" max="1" step="0.01" v-model="interfaceConfig.simulation.friction"
                thumb-label></v-slider>

              <div class="text-caption">Decay</div>
              <v-slider min="100" max="10000" step="100" v-model="interfaceConfig.simulation.decay"
                thumb-label></v-slider>

              <div class="text-caption">Repulsion From Mouse</div>
              <v-slider min="0" max="5" step="0.1" v-model="interfaceConfig.simulation.repulsionFromMouse"
                thumb-label></v-slider>
            </v-expansion-panel-text>
          </v-expansion-panel>
        </v-expansion-panels></v-card-text></v-fade-transition>
  </v-card>
  <div ref="draggingElement" draggable="true" style="display: none; position: fixed; z-index: 100; top: 0">
    <v-icon icon="mdi-plus" size="2rem"></v-icon>
  </div>
</template>
<script setup>
import { ref, onMounted, watch, reactive, computed } from "vue";
import {
  useOrigFullGraphStore,
  useKNeighborStore,
  useAutoTreeStore,
  useCustomizedIMStore,
  useGraphologyStore,
} from "@/store/store.js";
import { Chart } from 'highcharts-vue';
//handle leading zeros
const formatPercentage = (number) => {
  const percentage = Number(number.toFixed(5).toString().substring(2, 4));
  if (percentage === 0) {
    return "0%";
  }
  return percentage.toString().replace(/^0+/, "") + "%";
};
//handle collapse toolbar
const showRightClickTooltip = ref(false);
const showWindowTooltip = ref(false);
const showBasicTooltip = ref(false);
const showOrigRenderBtnTooltip = ref(false);
const showKNeighborTooltip = ref(false);
const showAutoTreeTooltip = ref(false);
const showATRenderBtnTooltip = ref(false);
const showATDestoryBtnTooltip = ref(false);
const showSSMTooltip = ref(false);
const showSSMRenderBtnTooltip = ref(false);
const showIMTooltip = ref(false);
const showIMRenderBtnTooltip = ref(false);
const showIntegratedMethodsTooltip = ref(false);
const showIntegratedMethodsSubmitTooltip = ref(false);
const showHighlightCustomizedNodesFromMethodTooltip = ref(false);
const showPruneBtnTooltip = ref(false);
const showHighlightCustomizedNodesFromIPTooltip = ref(false);
const showTransferIPResultToRenderTooltip = ref(false);
const showCustomizedRenderingTooltip = ref(false);
const showHighlightCustomizedNodesTooltip = ref(false);
const showCustomizedIMRenderSubmitBtnTooltip = ref(false);
const showCustomizedIMRenderBtnTooltip = ref(false);
const showStepwiseVisualizationTooltip = ref(false);
const showRandomColorTooltip = ref(false);
const showClearShowRoundsTooltip = ref(false);
const showLayoutTooltip = ref(false);


const collapsed = ref(false);
const handleRightClick = (event) => {
  event.preventDefault(); // Prevent the context menu from appearing
  console.log("Right-click or long-press detected!");
  collapsed.value = !collapsed.value;
};
const titleWidth = computed(() => (collapsed.value ? "auto" : "50vh"));
//// emits
const emit = defineEmits(["addComponent", "removeComponent"]);
const addComponentEmit = () => {
  const index = addedWindowNameList.value.indexOf(windowSelected.value);
  if (index > -1) {
    hasWindowSnackbar.value = true;
  } else {
    addedWindowNameList.value.push(windowSelected.value);
    if (
      windowSelected.value !== "Degree Distribution" &&
      windowSelected.value !== "Metrics Report"
    ) {
      addedConfigs[windowSelected.value] = true;
      configItems.value = Object.keys(addedConfigs);
    }
    emit(
      "addComponent",
      windowSelected.value,
      rowHeightSelected.value,
      colWidthSelected.value
    );
    if (windowSelected.value == "K Neighbor") {
      origFullGraphStore.kNeighborEnabled = true;
    }
  }
};
const removeComponentEmit = () => {
  const index = addedWindowNameList.value.indexOf(windowSelected.value);
  if (index > -1) {
    addedWindowNameList.value.splice(index, 1);

    if (
      windowSelected.value !== "Degree Distribution" &&
      windowSelected.value !== "Metrics Report"
    ) {
      delete addedConfigs[windowSelected.value];
      configItems.value = Object.keys(addedConfigs);
    }
    emit("removeComponent", windowSelected.value);
    if (windowSelected.value == "K Neighbor") {
      origFullGraphStore.kNeighborEnabled = false;
    } else if (windowSelected.value == "AutoTree") {
      autoTreeCreated.value = false;
    } else if (windowSelected.value == "Customized IM") {
      //customizedIMStore.customizedIM.destroy();
      customizedIMStore.customizedIM = null;
      console.log("destroyed", customizedIMStore.customizedIM);
    }
  } else {
    noWindowSnackbar.value = true;
  }
};
//// stores
const origFullGraphStore = useOrigFullGraphStore();
const autoTreeStore = useAutoTreeStore();
const kNeighborStore = useKNeighborStore();
const customizedIMStore = useCustomizedIMStore();
const graphologyStore = useGraphologyStore();
//// snackbars
const autoTreeSnackbar = ref(false);
const customizedIMSnackbar = ref(false);
const kNeighborValueSnackbar = ref(false);
const hasWindowSnackbar = ref(false);
const noWindowSnackbar = ref(false);
const methodSeedHasReturnedSnackbar = ref(false);
const methodSeedFailedToReturnSnackbar = ref(false);
const ipSeedHasReturnedSnackbar = ref(false);
const ipSeedFailedToReturnSnackbar = ref(false);

//// dragging
const draggingElement = ref(null);
const buttonDragging = ref(false);
// ref dom elements for draggable div
// the value of ref is different in this case. It is the proxy of dom, so we need $el to get the real dom
const draggableDiv = ref(null);
// functions
// a helper function to show effects when drag toolbar
const makeToolBarDraggable = () => {
  let draggableDivParent = draggableDiv.value.$el.parentElement; // parent div that contains the draggable div: the real toolbar
  //Draggable Div
  //TODO: add Y axis dragging. When Y change, make it vertical
  // Initialize some variables
  let draggingDiv = false; // Whether the div is being dragged or not
  let mouseX, mouseY; // The mouse position relative to the document
  let offsetX, offsetY; // The offset of the div relative to the mouse
  //console.log(draggableDiv.value.$el);
  // Add a mousedown event listener to the div
  draggableDiv.value.$el.addEventListener("mousedown", function (e) {
    if (!buttonDragging.value) {
      //if not dragging button, then drag container
      // Set dragging to true
      console.log(
        "dragging toolbar with buttonDragging=",
        buttonDragging.value
      );
      draggingDiv = true;

      // Get the mouse position
      mouseX = e.clientX;
      mouseY = e.clientY;

      // Get the offset of the div
      offsetX = draggableDivParent.offsetLeft;
      offsetY = draggableDivParent.offsetTop;
    }
  });

  // Add a mousemove event listener to the document
  document.addEventListener("mousemove", function (e) {
    // If dragging is true
    if (draggingDiv) {
      // Calculate the new position of the div
      let newX = e.clientX - mouseX + offsetX;
      let newY = e.clientY - mouseY + offsetY;

      // Set the div's offset to the new position
      draggableDivParent.style.left = newX + "px";
      draggableDivParent.style.top = newY + "px";
    }
  });

  // Add a mouseup event listener to the document
  document.addEventListener("mouseup", function () {
    // Set dragging to false
    draggingDiv = false;
  });
};
//// window adder
const windowNameList = ref([
  "K Neighbor",
  "AutoTree",
  "Metrics Report",
  "Degree Distribution",
  "Customized IM",
]);
const addedWindowNameList = ref([]);
const windowSelected = ref("K Neighbor");
const rowHeightSelected = ref(1);
const colWidthSelected = ref(1);

//// config for layout target switch

const configType = ref("Original Graph");
const configs = reactive({
  origFullGraph: origFullGraphStore.origFullGraphConfig,
  autoTree: autoTreeStore.autoTreeConfig,
  kNeighbor: kNeighborStore.kNeighborConfig,
  customizedIM: customizedIMStore.customizedIMConfig,
});
const addedConfigs = reactive({ "Original Graph": true });
const configItems = ref(Object.keys(addedConfigs));

const interfaceConfig = computed(() => {
  let type = "origFullGraph";
  if (configType.value == "K Neighbor") {
    type = "kNeighbor";
  } else if (configType.value == "AutoTree") {
    type = "autoTree";
  } else if (configType.value == "Customized IM") {
    type = "customizedIM";
  }
  return configs[type];
});
const isRenderColorMap = ref(false);
const renderOrigColormap = () => {
  isRenderColorMap.value = true;
  origFullGraphStore.origColormapRender();
};
const renderSSMColormap = () => {
  isRenderColorMap.value = true;
  origFullGraphStore.ssmColormapRender();
};
const renderIMColormap = () => {
  isRenderColorMap.value = true;
  origFullGraphStore.imColormapRender();
};
const renderCustomizedIMColormap = () => {
  //TODO: check if useOrig
  if (!customizedIMStore.useNewContainer) {
    renderIMColormap();
    return;
  }
  const index = addedWindowNameList.value.indexOf("Customized IM");
  console.log("index is", index, "; customized im is", customizedIMStore.customizedIM);
  if (index > -1) {
    if (customizedIMStore.customizedIM === null || customizedIMStore.customizedIM === undefined) {
      customizedIMStore.customizedIMCreate();
    } else {
      isRenderColorMap.value = true;
      customizedIMStore.imColormapRender();
    }
  } else {
    customizedIMSnackbar.value = true;
  }
}; /*
watch(
  () => configType.value,
  (newValue) => {
    if (newValue == "kNeighbor") {
      // ... code to switch to kNeighborConfig
      console.log("switch to kNeighborConfig", newValue);
    } else {
      // ... code to switch toorigFullGraphConfig
      console.log("switch to origFullGraphConfig", newValue);
    }
  }
);*/
// watch for changes in full graph config
watch(
  () => origFullGraphStore.origFullGraphConfig,
  (newConfig) => {
    //console.log(origFullGraphConfig changed");
    //console.log(store.origFullGraph);
    configs.origFullGraph = origFullGraphStore.origFullGraphConfig;
    origFullGraphStore.origFullGraph.setConfig(newConfig);
    // if just render color, do not interrupt
    if (!isRenderColorMap.value) {
      origFullGraphStore.origFullGraph.start();
    } else {
      //update k neighbor if exist
      const index = addedWindowNameList.value.indexOf("K Neighbor");
      if (index > -1) {
        kNeighborStore.kNeighborColorMapRender();
      }
    }
    isRenderColorMap.value = false;
    //OrigFullGraph.fitView();
  },
  { deep: true }
);
//// watch kNeighbor config
watch(
  () => kNeighborStore.kNeighborConfig,
  (newConfig) => {
    //console.log("kNeighborConfig changed", newConfig);
    configs.kNeighbor = kNeighborStore.kNeighborConfig;
    kNeighborStore.kNeighbor.setConfig(newConfig);
    if (!isRenderColorMap.value) {
      kNeighborStore.kNeighbor.start();
    }
    isRenderColorMap.value = false;
  },
  { deep: true }
);
//// watch autoTree config
watch(
  () => autoTreeStore.autoTreeConfig,
  (newConfig) => {
    //console.log("autoTreeConfig changed", newConfig);
    configs.autoTree = autoTreeStore.autoTreeConfig;
    autoTreeStore.autoTree.setConfig(newConfig);
    if (!isRenderColorMap.value) {
      autoTreeStore.autoTree.start();
    }
    isRenderColorMap.value = false;
  },
  { deep: true }
);
//// watch customizedIM config
watch(
  () => customizedIMStore.customizedIMConfig,
  (newConfig) => {
    //console.log("customizedIMConfig changed", newConfig);
    configs.customizedIM = customizedIMStore.customizedIMConfig;
    customizedIMStore.customizedIM.setConfig(newConfig);
    if (!isRenderColorMap.value) {
      customizedIMStore.customizedIM.start();
    }
    isRenderColorMap.value = false;
  },
  { deep: true }
);
//// kNeighbor value adder
const addKValue = () => {
  kNeighborStore.kValue += 1;
};
const minusKValue = () => {
  if (kNeighborStore.kValue > 1) {
    kNeighborStore.kValue -= 1;
  } else {
    kNeighborValueSnackbar.value = true;
  }
};
//// autoTree graph creator
const autoTreeCreated = ref(false);
const asteroidDestroyed = ref(false);
const createATGraph = () => {
  const index = addedWindowNameList.value.indexOf("AutoTree");
  if (index > -1) {
    autoTreeCreated.value = true;
    autoTreeStore.autoTreeCreate();
  } else {
    autoTreeSnackbar.value = true;
  }
};
// destroy autoTree asteroid
const asteroidDestroy = () => {
  asteroidDestroyed.value = true;
  autoTreeStore.asteroidDestroy();
};
//// kneighbor k val watcher
watch(
  () => kNeighborStore.kValue, //TODOlno, use store instead. or solve the problem of new k
  (newVal) => {
    const index = addedWindowNameList.value.indexOf("K Neighbor");
    if (index > -1) {
      kNeighborStore.kNeighborUpdate(newVal);
    }
  },
  { deep: true }
);

//// im round shower helper
const visibleIMRange = ref([0, 1]);
const currentVisibleIMStep = ref(-1);
const incrementVisibleIMStep = () => {
  if (currentVisibleIMStep.value < MaxRound.value) {
    currentVisibleIMStep.value++;
    showRounds.value[currentVisibleIMStep.value] = true;
    showRoundHandler(currentVisibleIMStep.value);
  }
};
const decrementVisibleIMStep = () => {
  if (currentVisibleIMStep.value >= 0) {
    showRounds.value[currentVisibleIMStep.value] = false;
    showRoundHandler(currentVisibleIMStep.value);
    currentVisibleIMStep.value--;
  }
};
watch(
  () => visibleIMRange.value,
  (newVal) => {
    let i = newVal[0];
    let j = newVal[1];
    for (let k = i; k <= j; k++) {
      showRounds.value[k] = true;
      showRoundHandler(k);
    }
  },
  { deep: true }
);
//// im round shower
const selectedIMGraph = ref(["Original"]);
const showRounds = ref({});
const clearShowRounds = () => {
  for (let round in Object.keys(currentimRoundColorDict.value)) {
    round = parseInt(round);
    showRounds.value[round] = false;
    showRoundHandler(round);
  }
  if (selectedIMGraph.value.includes("Original")) {
    origFullGraphStore.origFullGraph.unselectNodes();
  }
  if (selectedIMGraph.value.includes("Competitor")) {
    customizedIMStore.customizedIM.unselectNodes();
  }
  currentVisibleIMStep.value = -1;
};
const showRoundHandler = (round) => {
  if (selectedIMGraph.value.includes("Original")) {
    origFullGraphStore.imColormapRoundSelect(round, showRounds.value[round]);
  }
  if (selectedIMGraph.value.includes("Competitor")) {
    customizedIMStore.imColormapRoundSelect(round, showRounds.value[round]);
  }
};
const randomColorGenerator = () => {
  if (addedWindowNameList.value.includes("Customized IM")) {
    customizedIMStore.imColormapCreate(null, false, false);
  }
  origFullGraphStore.imColormapCreate(null, false, false);
};
const currentimRoundColorDict = computed(() => {
  const origDict = origFullGraphStore.imRoundColorDict;
  const customDict = customizedIMStore.imRoundColorDict;
  const getMaxKey = (dict) => Math.max(...Object.keys(dict).map(Number));
  const origMaxKey = getMaxKey(origDict);
  const customMaxKey = getMaxKey(customDict);
  // Return the dictionary with the larger max key
  return customMaxKey > origMaxKey ? customDict : origDict;
});
const MaxRound = computed(() => {
  return Math.max(...Object.keys(currentimRoundColorDict.value).map(Number));
});

watch(
  currentimRoundColorDict,
  (newDict) => {
    console.log("imRoundColorDict changed", newDict);
    for (const round in newDict) {
      if (!Object.prototype.hasOwnProperty.call(showRounds.value, round)) {
        showRounds.value[round] = false;
      }
    }
  },
  { deep: true }
);
console.log();
/// IM customized render
const selectedNodesForIM = ref([]);
const selectedNodesForIMFallbackSnackbar = ref(false);
const spreadProbability = ref(20);
const spreadModel = ref('IC');
const timeLimit = ref(5);
// highlight selected nodes TODO: highlight on orig or customized
const highlightCustomizedNodes = () => {
  origFullGraphStore.origFullGraph.selectNodesByIds(selectedNodesForIM.value);
};
//// check node validaty (rely on bug to perform "input twice for deletion". Actually a tricky case but I don have time to check logic)
watch(selectedNodesForIM, (newVal, oldVal) => {
  if (isMethodInput.value) {
    isMethodInput.value = false;
  }
  else {
    currentMethodName.value = "N/A";
    currentMethodParameters.value = "N/A";
  }
  // if delete
  if (oldVal.length > newVal.length) {
    return;
  } else if (oldVal.length + 1 == newVal.length) {
    const newNode = newVal[newVal.length - 1];
    let found = false;
    const nodeIDs = new Set(origFullGraphStore.nodeList.map((item) => item.id));
    if (nodeIDs.has(newNode)) {
      //console.log("found", newNode);
      found = true;
    }
    if (!found) {
      selectedNodesForIMFallbackSnackbar.value = true;
      selectedNodesForIM.value = oldVal;
    }
  }
});
watch(
  () => origFullGraphStore.selectedNode,
  (newVal) => {
    if (newVal !== undefined) {
      if (selectedNodesForIM.value.includes(newVal)) {
        return;
      }
      selectedNodesForIM.value.push(newVal);
    }
  }
);
//// deal with server im result check
const customizedIMSubmit = async () => {
  customizedIMStore.hasReceived = false;
  if (
    selectedNodesForIM.value.length < 1 ||
    spreadProbability.value <= 0 ||
    spreadProbability.value > 100
  ) {
    selectedNodesForIMFallbackSnackbar.value = true;
    return;
  }
  try {
    const customizedIMResponse = await fetch(
      "http://localhost:4000/customizedIM",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          nodes: selectedNodesForIM.value,
          spreadModel: spreadModel.value,
          spreadProbability: spreadProbability.value,
          timeLimit: timeLimit.value
        }),
      }
    );
    console.log(
      "CustomizedIM server responded"
    );
    //console.log('nodelist', selectedNodesForIM.value);
    const degreeCentralityList = graphologyStore.getNodeListAttr(selectedNodesForIM.value, 'degreeCentrality');
    const eigenvectorCentralityList = graphologyStore.getNodeListAttr(selectedNodesForIM.value, 'eigenvectorCentrality');
    const pagerankList = graphologyStore.getNodeListAttr(selectedNodesForIM.value, 'pagerank');
    const metricsResponse = await fetch(
      "http://localhost:4000/metrics",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          nodes: selectedNodesForIM.value,
          spreadProbability: spreadProbability.value,
        }),
      }
    );
    const metricsJson = await metricsResponse.json();
    //currently only cascade
    const cascadeList = metricsJson.data.sort((a, b) => Number(b) - Number(a));
    const getSum = (lst) => { return lst.reduce((a, b) => a + b) };
    let summationList = [];
    summationList.push(getSum(degreeCentralityList));
    summationList.push(getSum(eigenvectorCentralityList));
    summationList.push(getSum(pagerankList));
    summationList.push(getSum(cascadeList));
    console.log("old", degreeCentralityList, eigenvectorCentralityList, cascadeList);
    if (customizedIMStore.useNewContainer) {
      rightMethodName.value = currentMethodName.value;
      rightMethodParameters.value = currentMethodParameters.value;
      binaryComparisonOptionList.value['degreeCentrality'].series[1].data = degreeCentralityList;
      binaryComparisonOptionList.value['eigenvectorCentrality'].series[1].data = eigenvectorCentralityList;
      binaryComparisonOptionList.value['pagerank'].series[1].data = pagerankList;
      binaryComparisonOptionList.value['cascade'].series[1].data = cascadeList;
      summationComparisonOption.value.series[1].data = summationList;
      currentMethodParameters.value = "";
      currentMethodName.value = "";
      //isMethodInput.value = false;
    }
    else {
      leftMethodName.value = currentMethodName.value;
      leftMethodParameters.value = currentMethodParameters.value;
      binaryComparisonOptionList.value['degreeCentrality'].series[0].data = degreeCentralityList;
      binaryComparisonOptionList.value['eigenvectorCentrality'].series[0].data = eigenvectorCentralityList;
      binaryComparisonOptionList.value['pagerank'].series[0].data = pagerankList;
      binaryComparisonOptionList.value['cascade'].series[0].data = cascadeList;
      summationComparisonOption.value.series[0].data = summationList;
      currentMethodParameters.value = "";
      currentMethodName.value = "";
    }
    console.log("new", binaryComparisonOptionList.value);
  } catch (error) {
    console.error(error);
  }
};
//// deal with IM methods client-server exchange
const methodInputInvalidSnackbar = ref(false);
const isDIYParameters = ref(false);
const diyParameters = ref("");
const methodTypeList = ref(["PMC", "Subsim", "Game", "SSA", "DSSA"]);
const methodType = ref("PMC");
const methodSeedSize = ref(10);
const pmcDecay = ref(100);
const subsimPdistList = ref(["wc", "uniform", "skewed"]);
const subsimPdist = ref("wc");
const subsimWCVariant = ref(1.2);
const subsimPedge = ref(0.1);
const subsimSkewedDist = ref("exp");
const subsimEps = ref(0.1);
const subsimDelta = ref(0.0002);
const subsimVanilla = ref("Subsim");
const subsimHist = ref("False");
const ssaEpsilon = ref(0.1);
const ssaDelta = ref(0.01);
const ssaModelList = ref(["LT", "IC"]);
const ssaModel = ref("LT");
const selectedNodesFromMethod = ref([]);
const highlightCustomizedNodesFromMethod = () => {
  origFullGraphStore.origFullGraph.selectNodesByIds(
    selectedNodesFromMethod.value
  );
};
const methodSubmit = async () => {
  if (methodType.value == "PMC") {
    pmcSubmit();
  } else if (methodType.value == "Subsim") {
    subsimSubmit();
  } else if (methodType.value == "Game") {
    gameSubmit();
  } else if (methodType.value == "SSA" || methodType.value == "DSSA") {
    ssaSubmit(methodType.value);
  }
};
const pmcSubmit = async () => {
  //if(!isDIYParameters.value)
  if (
    pmcDecay.value <= 0 ||
    parseInt(methodSeedSize.value) <= 0 ||
    parseInt(methodSeedSize.value) > parseInt(origFullGraphStore.nodeNum) ||
    spreadProbability.value > 100 ||
    spreadProbability.value < 0
  ) {
    methodInputInvalidSnackbar.value = true;
    return;
  }
  try {
    console.log("Asking for PMC...");
    const params = JSON.stringify({
      size: methodSeedSize.value,
      decay: pmcDecay.value,
      spreadProbability: spreadProbability.value,
      isDIYParameters: isDIYParameters.value,
      diyParameters: diyParameters.value,
    }).replace(/,/g, ',\n');
    const pmcResponse = await fetch("http://localhost:4000/pmc", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: params,
    });
    // here we directly exchange between one thread.
    const pmcSeedsJson = await pmcResponse.json();
    console.log("pmc seed", pmcSeedsJson.data);
    selectedNodesFromMethod.value = pmcSeedsJson.data;
    isMethodInput.value = true;
    currentMethodName.value = "PMC";
    currentMethodParameters.value = params;
    selectedNodesForIM.value = pmcSeedsJson.data;
    methodSeedHasReturnedSnackbar.value = true;
  } catch (error) {
    methodSeedFailedToReturnSnackbar.value = true;
    console.error(error);
  }
};
const subsimSubmit = async () => {
  //if(!isDIYParameters.value)
  if (
    parseInt(methodSeedSize.value) <= 0 ||
    parseInt(methodSeedSize.value) > parseInt(origFullGraphStore.nodeNum)
  ) {
    methodInputInvalidSnackbar.value = true;
    return;
  }
  try {
    console.log("Asking for Subsim...");
    const params = JSON.stringify({
      size: methodSeedSize.value,
      pdist: subsimPdist.value,
      isDIYParameters: isDIYParameters.value,
      diyParameters: diyParameters.value,
      wcvariant: subsimWCVariant.value,
      pedge: subsimPedge.value,
      skew: subsimSkewedDist.value,
      eps: subsimEps.value,
      delta: subsimDelta.value,
      vanilla: Number(subsimVanilla.value == "Vanilla"),
      hist: Number(subsimHist.value == "True"),
    }).replace(/,/g, ',\n');
    const subsimResponse = await fetch("http://localhost:4000/subsim", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: params,
    });
    // here we directly exchange between one thread.
    const subsimSeedsJson = await subsimResponse.json();
    console.log("subsim seed", subsimSeedsJson.data);
    selectedNodesFromMethod.value = subsimSeedsJson.data;
    isMethodInput.value = true;
    currentMethodName.value = "Subsim";
    currentMethodParameters.value = params;
    selectedNodesForIM.value = subsimSeedsJson.data;
    methodSeedHasReturnedSnackbar.value = true;
  } catch (error) {
    methodSeedFailedToReturnSnackbar.value = true;
    console.error(error);
  }
};

const gameSubmit = async () => {
  //if(!isDIYParameters.value)
  if (
    parseInt(methodSeedSize.value) <= 0 ||
    parseInt(methodSeedSize.value) > parseInt(origFullGraphStore.nodeNum)
  ) {
    methodInputInvalidSnackbar.value = true;
    return;
  }
  try {
    console.log("Asking for Game...");
    const params = JSON.stringify({
      size: methodSeedSize.value,
      isDIYParameters: isDIYParameters.value,
      diyParameters: diyParameters.value,
    }).replace(/,/g, ',\n');
    const gameResponse = await fetch("http://localhost:4000/game", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: params,
    });
    // here we directly exchange between one thread.
    const gameSeedsJson = await gameResponse.json();
    console.log("pmc seed", gameSeedsJson.data);
    selectedNodesFromMethod.value = gameSeedsJson.data;
    isMethodInput.value = true;
    currentMethodName.value = "Game";
    currentMethodParameters.value = params;
    selectedNodesForIM.value = gameSeedsJson.data;
    methodSeedHasReturnedSnackbar.value = true;
  } catch (error) {
    methodSeedFailedToReturnSnackbar.value = true;
    console.error(error);
  }
};
// seedsize, epsilon, delta, model, isDSSA
const ssaSubmit = async (ssaType) => {
  //if(!isDIYParameters.value)
  if (
    pmcDecay.value <= 0 ||
    parseInt(methodSeedSize.value) <= 0 ||
    parseInt(methodSeedSize.value) > parseInt(origFullGraphStore.nodeNum)
  ) {
    methodInputInvalidSnackbar.value = true;
    return;
  }
  try {
    console.log("Asking for SSA/DSSA...");
    const params = JSON.stringify({
      size: methodSeedSize.value,
      epsilon: ssaEpsilon.value,
      delta: ssaDelta.value,
      model: ssaModel.value,
      isDSSA: ssaType, //got from parameter
      isDIYParameters: isDIYParameters.value,
      diyParameters: diyParameters.value,
    }).replace(/,/g, ',\n');
    const ssaResponse = await fetch("http://localhost:4000/ssa", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: params,
    });
    // here we directly exchange between one thread.
    const ssaSeedsJson = await ssaResponse.json();
    console.log("pmc seed", ssaSeedsJson.data);
    selectedNodesFromMethod.value = ssaSeedsJson.data;
    isMethodInput.value = true;
    currentMethodName.value = ssaType;
    currentMethodParameters.value = params;
    selectedNodesForIM.value = ssaSeedsJson.data;
    methodSeedHasReturnedSnackbar.value = true;
  } catch (error) {
    methodSeedFailedToReturnSnackbar.value = true;
    console.error(error);
  }
};
//// deal with ip client-server exchange
const selectedNodesFromIP = ref([]);
const selectedNodesFromIPFallbackSnackbar = ref(false);
const prunedNodesFromIP = ref([]);
const newNodesFromIP = ref([]);
const highlightCustomizedNodesFromIP = () => {
  origFullGraphStore.origFullGraph.selectNodesByIds(selectedNodesFromIP.value);
};
const ipSubmit = async () => {
  if (selectedNodesFromMethod.value.length < 1) {
    methodInputInvalidSnackbar.value = true;
    return;
  }
  try {
    console.log("Asking for IP...");
    const ipResponse = await fetch("http://localhost:4000/ip", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        nodes: selectedNodesFromMethod.value,
      }),
    });
    // here we directly exchange between one thread.
    const ipSeedsJson = await ipResponse.json();
    console.log("ip seed", ipSeedsJson.data);
    selectedNodesFromIP.value = ipSeedsJson.data;
    prunedNodesFromIP.value = selectedNodesFromMethod.value.filter(
      (x) => selectedNodesFromIP.value.indexOf(x) === -1
    );
    newNodesFromIP.value = selectedNodesFromIP.value.filter(
      (x) => selectedNodesFromMethod.value.indexOf(x) === -1
    );
    ipSeedHasReturnedSnackbar.value = true;
  } catch (error) {
    ipSeedFailedToReturnSnackbar.value = true;
    console.error(error);
  }
};
const hasRetrievedDataSnackbar = ref(false);
const transferIPResultToRender = () => {
  isMethodInput.value = true;
  if (currentMethodName.value === "") {
    currentMethodName.value = "N/A\n+Prune";
  }
  else {
    currentMethodName.value += "\n+Prune";
  }
  currentMethodParameters.value = "[Pruned]\n" + currentMethodParameters.value;
  selectedNodesForIM.value = selectedNodesFromIP.value;
  hasRetrievedDataSnackbar.value = true;
};

//// stepwise table detail
const leftMethodName = ref("PMC");
const rightMethodName = ref("");
const leftMethodParameters = ref("Default");
const rightMethodParameters = ref("");
const currentMethodName = ref("");
const currentMethodParameters = ref("");
const isMethodInput = ref(false);

//// user uploaded method
const uploadMethodDialog = ref(false);
const uploadMethodName = ref("");
const uploadMethodCommand = ref("");
const newMethodSubmit = () => {
  console.log(uploadMethodCommand.value);
}

//// seed set comparison
const seedSetComparisonDialog = ref(false);
const binaryComparisonOptionList = ref({
  'degreeCentrality': {
    series: [
      {
        name: 'LHS',
        data: []
      },
      {
        name: "RHS",
        data: []
      }
    ],
    credits: {
      enabled: false,
    },
    chart: {
      zoomType: "xy",
    },
    title: {
      text: "",
    },
    subtitle: {
      text: "",
    },
    tooltip: {
      headerFormat:
        '<span style="font-size:10px">{point.key}</span><br><table>',
      footerFormat: "</table>",
      shared: true,
    },
    legend: {
      floating: false,
    },
    exporting: {
      buttons: {
        contextButton: {
          x: -15, // move the button 10 pixels to the left
          y: -7, // move the button 10 pixels down
          symbol: "menu",
        },
      },
    },
  },
  'eigenvectorCentrality': {
    series: [
      {
        name: 'LHS',
        data: []
      },
      {
        name: "RHS",
        data: []
      }
    ],
    credits: {
      enabled: false,
    },
    chart: {
      zoomType: "xy",
    },
    title: {
      text: "",
    },
    subtitle: {
      text: "",
    },
    tooltip: {
      headerFormat:
        '<span style="font-size:10px">{point.key}</span><br><table>',
      footerFormat: "</table>",
      shared: true,
    },
    legend: {
      floating: false,
    },
    exporting: {
      buttons: {
        contextButton: {
          x: -15, // move the button 10 pixels to the left
          y: -7, // move the button 10 pixels down
          symbol: "menu",
        },
      },
    },
  },
  'pagerank': {
    series: [
      {
        name: 'LHS',
        data: []
      },
      {
        name: "RHS",
        data: []
      }
    ],
    credits: {
      enabled: false,
    },
    chart: {
      zoomType: "xy",
    },
    title: {
      text: "",
    },
    subtitle: {
      text: "",
    },
    tooltip: {
      headerFormat:
        '<span style="font-size:10px">{point.key}</span><br><table>',
      footerFormat: "</table>",
      shared: true,
    },
    legend: {
      floating: false,
    },
    exporting: {
      buttons: {
        contextButton: {
          x: -15, // move the button 10 pixels to the left
          y: -7, // move the button 10 pixels down
          symbol: "menu",
        },
      },
    },
  },
  'cascade': {
    series: [
      {
        name: 'LHS',
        data: []
      },
      {
        name: "RHS",
        data: []
      }
    ],
    credits: {
      enabled: false,
    },
    chart: {
      zoomType: "xy",
    },
    title: {
      text: "",
    },
    subtitle: {
      text: "",
    },
    tooltip: {
      headerFormat:
        '<span style="font-size:10px">{point.key}</span><br><table>',
      footerFormat: "</table>",
      shared: true,
    },
    legend: {
      floating: false,
    },
    exporting: {
      buttons: {
        contextButton: {
          x: -15, // move the button 10 pixels to the left
          y: -7, // move the button 10 pixels down
          symbol: "menu",
        },
      },
    },
  }
});
const binaryComparisonOption = ref('degreeCentrality');
const summationComparisonOption = ref({
  series: [{
    name: 'LHS',
    type: 'column',
    data: []
  },
  {
    name: 'RHS',
    type: 'column',
    data: []
  }],
  credits: {
    enabled: false,
  },
  chart: {
    zoomType: "xy",
  },
  title: {
    text: "",
  },
  subtitle: {
    text: "",
  },
  xAxis: [
    {
      categories: ['degreeCentrality', 'eigenvectorCentrality', 'pagerank', 'cascade'],
      crosshair: true,
    },
  ],
  tooltip: {
    headerFormat:
      '<span style="font-size:10px">{point.key}</span><br><table>',
    footerFormat: "</table>",
    shared: true,
  },
  exporting: {
    buttons: {
      contextButton: {
        x: -15, // move the button 10 pixels to the left
        y: -7, // move the button 10 pixels down
        symbol: "menu",
      },
    },
  },
})
onMounted(() => {
  makeToolBarDraggable();
});
</script>
<style>
.center-checkbox {
  justify-content: center;
}

.center-checkbox * {
  justify-content: center;
}

.collapsed {
  max-height: none !important;
  width: 64px !important;
}

.collapsed-icon {
  position: absolute;
  right: 0;
  top: 0;
  z-index: 11;
  cursor: pointer;
}

/* Set the width and height of the scrollbar */
::-webkit-scrollbar {
  width: 2px;
  height: 2px;
}

/* Track */
::-webkit-scrollbar-track {
  background: #f1f1f1;
}

/* Handle */
::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 0;
}

/* Handle on hover */
::-webkit-scrollbar-thumb:hover {
  background: #555;
}

/* handle seletable*/
.not-selectable {
  -webkit-touch-callout: none;
  -webkit-user-select: none;
  -khtml-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}
</style>
