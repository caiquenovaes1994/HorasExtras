
import {Fragment,memo,useContext,useEffect} from "react"
import {isTrue} from "$/utils/state"
import {StateContexts} from "$/utils/context"
import {jsx} from "@emotion/react"






export const Cond_comp_5ac944a1db343fc65190e1319707e741 = memo(({children}) => {
    const reflex___state____state__sandbox_reflex___state____auth_state = useContext(StateContexts.reflex___state____state__sandbox_reflex___state____auth_state)



    return(
        ((reflex___state____state__sandbox_reflex___state____auth_state.user_info_rx_state_?.["perfil"]?.valueOf?.() === "ADMIN"?.valueOf?.())?(children?.at?.(0)):(children?.at?.(1)))
    )
});
