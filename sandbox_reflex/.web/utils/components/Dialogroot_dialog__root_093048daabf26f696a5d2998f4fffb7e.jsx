
import {Fragment,memo,useContext,useEffect} from "react"
import {isTrue} from "$/utils/state"
import {Dialog as RadixThemesDialog} from "@radix-ui/themes"
import {StateContexts} from "$/utils/context"
import {jsx} from "@emotion/react"






export const Dialogroot_dialog__root_093048daabf26f696a5d2998f4fffb7e = memo(({children}) => {
    const reflex___state____state__sandbox_reflex___state_form____form_state = useContext(StateContexts.reflex___state____state__sandbox_reflex___state_form____form_state)



    return(
        jsx(RadixThemesDialog.Root,{open:reflex___state____state__sandbox_reflex___state_form____form_state.is_modal_open_rx_state_},children)
    )
});
