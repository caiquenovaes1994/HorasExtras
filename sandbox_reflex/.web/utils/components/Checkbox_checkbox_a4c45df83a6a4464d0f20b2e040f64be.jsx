
import {Fragment,memo,useCallback,useContext,useEffect} from "react"
import {ReflexEvent,applyEventActions,isTrue} from "$/utils/state"
import {Checkbox as RadixThemesCheckbox} from "@radix-ui/themes"
import {EventLoopContext,StateContexts} from "$/utils/context"
import {jsx} from "@emotion/react"






export const Checkbox_checkbox_a4c45df83a6a4464d0f20b2e040f64be = memo(({children}) => {
    const [addEvents, connectErrors] = useContext(EventLoopContext);
const on_change_14f7f9a63db1c055aaba52a9af05a2dc = useCallback(((_ev_0) => (addEvents([(ReflexEvent("reflex___state____state.sandbox_reflex___state____auth_state.sandbox_reflex___data_state____data_state.toggle_select_all", ({ ["checked"] : _ev_0 }), ({  })))], [_ev_0], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__sandbox_reflex___state____auth_state__sandbox_reflex___data_state____data_state = useContext(StateContexts.reflex___state____state__sandbox_reflex___state____auth_state__sandbox_reflex___data_state____data_state)



    return(
        jsx(RadixThemesCheckbox,{checked:reflex___state____state__sandbox_reflex___state____auth_state__sandbox_reflex___data_state____data_state.is_all_selected_rx_state_,onCheckedChange:on_change_14f7f9a63db1c055aaba52a9af05a2dc,size:"2"},)
    )
});
