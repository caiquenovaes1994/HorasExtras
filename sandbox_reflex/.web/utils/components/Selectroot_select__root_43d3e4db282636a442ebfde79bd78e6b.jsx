
import {Fragment,memo,useCallback,useContext,useEffect} from "react"
import {ReflexEvent,applyEventActions,isTrue} from "$/utils/state"
import {Select as RadixThemesSelect} from "@radix-ui/themes"
import {EventLoopContext,StateContexts} from "$/utils/context"
import {jsx} from "@emotion/react"






export const Selectroot_select__root_43d3e4db282636a442ebfde79bd78e6b = memo(({children}) => {
    const [addEvents, connectErrors] = useContext(EventLoopContext);
const on_change_6059bac5fb1c629dbda5e0feb7978c8f = useCallback(((_ev_0) => (addEvents([(ReflexEvent("reflex___state____state.sandbox_reflex___state_usuarios____usuario_state.set_u_perfil", ({ ["val"] : _ev_0 }), ({  })))], [_ev_0], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__sandbox_reflex___state_usuarios____usuario_state = useContext(StateContexts.reflex___state____state__sandbox_reflex___state_usuarios____usuario_state)



    return(
        jsx(RadixThemesSelect.Root,{onValueChange:on_change_6059bac5fb1c629dbda5e0feb7978c8f,value:reflex___state____state__sandbox_reflex___state_usuarios____usuario_state.u_perfil_rx_state_},children)
    )
});
