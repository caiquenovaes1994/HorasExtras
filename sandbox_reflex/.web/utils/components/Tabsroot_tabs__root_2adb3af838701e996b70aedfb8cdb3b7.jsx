
import {Fragment,memo,useCallback,useContext,useEffect} from "react"
import {ReflexEvent,applyEventActions,isTrue} from "$/utils/state"
import {Tabs as RadixThemesTabs} from "@radix-ui/themes"
import {EventLoopContext,StateContexts} from "$/utils/context"
import {jsx} from "@emotion/react"






export const Tabsroot_tabs__root_2adb3af838701e996b70aedfb8cdb3b7 = memo(({children}) => {
    const [addEvents, connectErrors] = useContext(EventLoopContext);
const on_change_b552394f092eec9225d3c0904ec45826 = useCallback(((_ev_0) => (addEvents([(ReflexEvent("reflex___state____state.sandbox_reflex___state____auth_state.sandbox_reflex___data_state____data_state.set_active_tab", ({ ["tab"] : _ev_0 }), ({  })))], [_ev_0], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__sandbox_reflex___state____auth_state__sandbox_reflex___data_state____data_state = useContext(StateContexts.reflex___state____state__sandbox_reflex___state____auth_state__sandbox_reflex___data_state____data_state)



    return(
        jsx(RadixThemesTabs.Root,{css:({ ["&[data-orientation='vertical']"] : ({ ["display"] : "flex" }), ["width"] : "100%" }),onValueChange:on_change_b552394f092eec9225d3c0904ec45826,value:reflex___state____state__sandbox_reflex___state____auth_state__sandbox_reflex___data_state____data_state.active_tab_rx_state_},children)
    )
});
