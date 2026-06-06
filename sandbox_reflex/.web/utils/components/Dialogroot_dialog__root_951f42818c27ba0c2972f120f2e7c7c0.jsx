
import {Fragment,memo,useContext,useEffect} from "react"
import {isTrue} from "$/utils/state"
import {Dialog as RadixThemesDialog} from "@radix-ui/themes"
import {StateContexts} from "$/utils/context"
import {jsx} from "@emotion/react"






export const Dialogroot_dialog__root_951f42818c27ba0c2972f120f2e7c7c0 = memo(({children}) => {
    const reflex___state____state__sandbox_reflex___state_usuarios____usuario_state = useContext(StateContexts.reflex___state____state__sandbox_reflex___state_usuarios____usuario_state)



    return(
        jsx(RadixThemesDialog.Root,{open:reflex___state____state__sandbox_reflex___state_usuarios____usuario_state.is_modal_open_rx_state_},children)
    )
});
