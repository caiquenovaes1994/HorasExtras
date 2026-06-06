
import {Fragment,memo,useContext,useEffect} from "react"
import {isTrue} from "$/utils/state"
import {StateContexts} from "$/utils/context"
import {jsx} from "@emotion/react"






export const Foreach_comp_47706282c8a78f4bd9fe25b0ba22339a = memo(({children}) => {
    const reflex___state____state__sandbox_reflex___state_form____form_state = useContext(StateContexts.reflex___state____state__sandbox_reflex___state_form____form_state)



    return(
        Array.prototype.map.call(reflex___state____state__sandbox_reflex___state_form____form_state.hoteis_opts_rx_state_ ?? [],((h_rx_state_,index_9ffd8f192f65aef79b77e0b7b8cefb00)=>(jsx("option",{key:index_9ffd8f192f65aef79b77e0b7b8cefb00,value:h_rx_state_},))))
    )
});
