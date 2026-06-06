
import {Fragment,memo,useContext,useEffect} from "react"
import {isTrue} from "$/utils/state"
import {StateContexts} from "$/utils/context"
import {jsx} from "@emotion/react"






export const Bare_comp_a970286e90e02de8bc833d512162b984 = memo(({children}) => {
    const reflex___state____state__sandbox_reflex___state____auth_state = useContext(StateContexts.reflex___state____state__sandbox_reflex___state____auth_state)



    return(
        ("@"+reflex___state____state__sandbox_reflex___state____auth_state.user_info_rx_state_?.["username"]+" - "+reflex___state____state__sandbox_reflex___state____auth_state.user_info_rx_state_?.["perfil"])
    )
});
